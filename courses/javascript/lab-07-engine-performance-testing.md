# Lab 07 — Engines, Memory, and Tests: How V8 Runs Your Code, and How You Prove It Works

> "Make it work, make it right, make it fast — in that order, and never skip the middle one."
> — Kent Beck, paraphrased

**Weeks:** 13–14 · **Language / runtime focus:** how V8 executes JavaScript — parsing, bytecode, JIT tiers, hidden classes and inline caches, deoptimization; garbage collection and why it hitches frames; allocation pressure and object pooling; typed arrays for hot data; Chrome DevTools Performance and Memory panels; Web Workers; testing with Vitest, fast-check, and Playwright; ESLint/Prettier or Biome; CI · **Project step:** a real test suite, a GC-hitch-free render loop, bots, and a server load test · **Course:** [JavaScript — Build a Multiplayer Game](README.md) · **Previous:** [Lab 06](lab-06-typescript.md)

---

## This lab's feature

Two things separate a project from a product: **you can prove it works**, and **you know why it's fast** — or why it isn't. This lab does both, and they're connected: profiling without tests means optimizing blindly, and tests without profiling means shipping something that stutters.

On the *engine* side you'll finally look inside V8: why an object that always has the same shape is fast and one that doesn't is slow; why `bullets.push(new Bullet())` 200 times a second causes a 30 ms pause every few seconds; what "JIT" and "deopt" mean in a language with no compile step. These are the topics of senior JavaScript interviews, and they are also *practical* — you'll fix a real frame hitch in your game by understanding them.

On the *testing* side you'll build the suite a professional codebase has: fast unit tests for the simulation, property-based tests for the protocol, a two-browser end-to-end test, and CI that runs it all. Your deterministic simulation from Lab 1 and typed protocol from Lab 6 make this almost pleasant.

---

## Theory

### 1. How V8 runs JavaScript

There is a compile step; it just happens at runtime. V8 **parses** source to an AST, compiles it to **bytecode** (the *Ignition* interpreter), and starts running immediately. Meanwhile it **profiles**: which functions run often, what types they see. Hot functions are recompiled by an optimizing **JIT** compiler (*TurboFan*, with the mid-tier *Maglev* in between) into machine code **specialized for the types observed** — a `add(a, b)` that has only ever seen integers compiles to an integer add. If an assumption is later violated (`add("a", 1)`), the optimized code is thrown away — a **deoptimization** — and execution falls back to bytecode. Franziska Hinkelmann's talk covers this pipeline in 30 minutes; Lydia Hallie's article is the illustrated version.

The practical rule: **be predictable**. Functions that always receive the same types and objects that always have the same shape stay optimized. Polymorphic code — one function handling ships, bullets, and asteroids with different fields — is slower not because of the branches but because the JIT can't specialize.

### 2. Hidden classes, shapes, and inline caches

V8 doesn't store objects as hash maps (that would be slow). Objects created the same way share a **hidden class** (a "shape" or "map"): a description of which properties exist at which offsets. `{ x, y }` has one shape; adding `.z` later transitions to a *different* shape. Property access `obj.x` at a call site is cached by shape — an **inline cache (IC)**. If the site always sees one shape it's *monomorphic* (fast: one check, one load). Two to four shapes: *polymorphic* (slower). More: *megamorphic* (a hash lookup every time — the slow path). Mathias Bynens and Benedikt Meurer's [Shapes and Inline Caches](https://mathiasbynens.be/notes/shapes-ics) is the definitive article.

Consequences for game code: **initialize every property in the constructor, in the same order, every time** (never add properties later; never `delete`); keep arrays **homogeneous** (all numbers, or all the same object shape — a "packed SMI array" or "packed double array" is a real V8 fast path, and mixing kinds, or leaving holes, demotes it); avoid `arguments` juggling and dynamic property names in hot paths. TypeScript's classes push you toward this naturally.

### 3. Garbage collection and the frame hitch

JavaScript allocates freely and V8 reclaims automatically with a **generational** collector (*Orinoco*): new objects go to the small **young generation**, collected often and fast (a *scavenge* — copying the few survivors, ~1 ms); objects that survive a couple of scavenges are promoted to the **old generation**, collected rarely with a **mark-sweep** that can pause for tens of milliseconds despite heavy parallelization and incremental marking. The [Trash Talk](https://v8.dev/blog/trash-talk) post from the V8 team explains the design.

A game at 60 fps allocating a few hundred objects per frame — bullets, particles, `{ x, y }` vectors from `Vector2.add`, closures, spread copies, `[...world]` — generates megabytes per second of garbage. Scavenges every few frames are fine; but survivors (a particle that lived 3 s) get promoted, the old generation fills, and a major GC lands in the middle of a frame. Visible as a **periodic hitch**, diagnosable in DevTools as a sawtooth heap graph and yellow/grey GC blocks in the flame chart.

The fixes are old and effective: **allocate less in hot paths** (in-place vector ops for the sim loop, reusing scratch objects), **object pooling** (Nystrom's [Object Pool](https://gameprogrammingpatterns.com/object-pool.html): preallocate bullets/particles, recycle instead of `new`), and **typed arrays** for bulk numeric state (`Float32Array` positions never allocate per element and give the engine a dense, homogeneous layout). Measure first — pooling everything is premature; pooling the two allocation hot spots the profiler shows is engineering.

### 4. Profiling: the Performance and Memory panels

Chrome DevTools → **Performance**: record 10 s of play; read the **frames** track (red = dropped), the **main-thread flame chart** (which functions took the time — your `render`, `step`, `collide`, and GC blocks), and the **Bottom-Up** view sorted by self time. Enable CPU throttling to simulate a weak laptop. `performance.mark("step:start")` / `performance.measure("step", …)` puts your own spans in the timeline (the User Timing track) — instrument `simulate`, `render`, `decode`, and `reconcile`. **Memory** → *Allocation instrumentation on timeline* shows *who* allocates during play; *Heap snapshot* diffs find leaks (entities never removed from a `Map`, listeners never `off`'d). The [Performance panel docs](https://developer.chrome.com/docs/devtools/performance) and [Fix memory problems](https://developer.chrome.com/docs/devtools/memory-problems) are practical guides.

On the server, `node --cpu-prof server.ts` writes a `.cpuprofile` you open in DevTools; `--heap-prof` for allocations; `process.memoryUsage()` and `performance.eventLoopUtilization()` for a live health picture — expose both on `/api/stats`.

**Benchmark methodology** (same rules as any language): warm up (the JIT needs iterations), repeat, report median and p95/p99 — not mean; change one thing at a time; keep the numbers in the README with the environment noted.

### 5. Web Workers: the second thread you're allowed

The main thread paints; anything heavy on it costs frames. **Web Workers** run JavaScript on another thread with **no shared memory by default** — you communicate by `postMessage`, which **structured-clones** the data (copy cost proportional to size), or by **transferring** an `ArrayBuffer` (zero-copy; the sender loses access), or by **`SharedArrayBuffer`** + `Atomics` (true shared memory; requires cross-origin isolation headers). `OffscreenCanvas` even lets a worker render. Candidates in your game: the particle system, a spatial hash rebuild, decoding large replays, bot AI. The trade-off is real: message latency and copy costs can exceed the work saved; measure. Node's equivalent is `worker_threads`.

### 6. Testing: Vitest, fast-check, Playwright

**Vitest** — Vite-native, Jest-compatible API (`describe`/`it`/`expect`), fast, runs TypeScript directly, watch mode, coverage. Your `shared/` sim is a gift to test: pure functions with fixed `dt` and a seeded PRNG — `step(world, inputs)` → assert positions; collision cases; the reconciliation algorithm as a pure function of (state, buffer, snapshot). **Fake timers** (`vi.useFakeTimers()`) test the loop's accumulator and the heartbeat logic without waiting. `vi.mock` isolates the WebSocket; but prefer *designing for testability* — inject the socket, don't mock the module.

**Property-based testing** with [fast-check](https://fast-check.dev): instead of examples, state invariants and let the library generate thousands of inputs and *shrink* failures to minimal cases. Your protocol is the perfect target: `decode(encode(m))` ≈ `m` for *any* valid message (with quantization tolerance); `encode` output length matches the spec; malformed buffers *never* throw anything but the expected error. Simulation invariants: energy bounded under drag; ships never leave the arena; determinism (`step` twice from a cloned state → identical results).

**Playwright** — real browsers, scripted: launch **two** browser contexts, both join one room, one flies toward the other, assert the second sees the first's ship move — an end-to-end test of client, server, and protocol together. Fifteen lines, and the most convincing test in the repo.

### 7. Lint, format, CI

**ESLint** (flat `eslint.config.js`, with `typescript-eslint`'s recommended-type-checked rules) catches floating promises, unused variables, and unsafe `any`; **Prettier** ends formatting debates. **Biome** does both in one fast tool — pick one. **GitHub Actions**: on every push, `npm ci` → `typecheck` → `lint` → `test` → `build` → Playwright (with `npx playwright install --with-deps chromium`). Cache `node_modules` by lockfile hash. Add a status badge. This is the workflow every JavaScript team has; get it green and keep it green.

### Prove it to yourself (DevTools + Node, 20 minutes)

1. `node --allow-natives-syntax -e "function add(a,b){return a+b}; for(let i=0;i<1e6;i++) add(i,1); %OptimizeFunctionOnNextCall(add); add(1,2); console.log(%GetOptimizationStatus(add)); add('a','b'); console.log(%GetOptimizationStatus(add))"` — decode the status bits (search "GetOptimizationStatus bits"). You just watched a deopt.
2. Two loops: one over `points = Array.from({length: 1e6}, (_, i) => ({ x: i, y: i }))`, another over the same but with every 10th object also having `.z`. Time `sum += p.x`. Then make it `Float32Array`s. Three numbers.
3. In your game, DevTools → Performance → record 10 s → find the GC blocks. Then Memory → allocation timeline → find the top allocator. Write down both before touching code.
4. `const w = new Worker(…)`: post a 50 MB `ArrayBuffer` with clone vs. with transfer; time both; check `buffer.byteLength` on the sender after each.
5. `fc.assert(fc.property(fc.float(), x => Math.fround(x) === x))` — does it pass? Now `fc.double()`. Read the shrunk counterexample.

---

## Project step: prove it, then make it fast

### Milestones

**M1 — The test suite.**
Vitest across all three packages (`npm test` at the root runs them all). **Unit**: `Vector2`; `integrate` with known inputs; collision cases (touching, overlapping, missing, fast bullet tunneling — does yours?); `World.step` determinism (clone, step both, deep-equal); reconciliation as a pure function; the token-bucket rate limiter; the accumulator loop with fake timers. **Property** (fast-check, ≥ 5 properties): codec round-trip within tolerance; codec length equals spec; arbitrary garbage buffers → typed error, never a crash; ships stay in-arena over 1,000 random input steps; `parseClientMessage` accepts every generated valid message and rejects every generated mutation of one. Aim for ≥ 60 tests; coverage on `shared/` ≥ 85 %.

**M2 — End-to-end and CI.**
Playwright: start the server (`webServer` config), open two contexts, join the same room, assert roster in both; fly one ship, assert the other context observes movement within 500 ms; send a chat, assert receipt. GitHub Actions running typecheck → lint → unit → build → e2e on push and PR, with a badge in the README. ESLint (type-checked rules) or Biome clean; `no-floating-promises` on — fix what it finds.

**M3 — Profile, fix the hitch, measure.**
Instrument `simulate`, `render`, `decode`, `reconcile` with `performance.mark/measure`. Record a 30-s session with **8 bots** (M4 — build them first if you like) and heavy shooting. Document *before*: frame-time p50/p95/p99 (compute from your Lab 1 frame-time samples), GC pause count and total, top three allocators, top three self-time functions, and a screenshot of the flame chart. Then fix, in order of measured impact — likely: **pool** bullets and particles; make `Vector2` hot paths allocation-free (in-place variants, or switch the sim's storage to `Float32Array`s); stop creating closures/arrays per frame in `render`; fix any megamorphic access the profiler shows (mixed entity shapes in one array → split by kind or normalize fields). *After*: the same table. Target: **zero major GCs during play and p99 frame time under 16.7 ms** on your machine with 8 bots. Server side: `--cpu-prof` a 60-s match; find the tick hot spot (likely O(n²) collision → spatial hash, or JSON logging); report tick-time p99 before/after.

**M4 — Bots, a worker, and a load test.**
**Bots**: server-side AI players (`Bot implements PlayerInput`) that chase, evade, and shoot — with the same input interface as humans (so the server can't tell) — and a `/api/rooms/:id/bots` endpoint to add N. Move **one subsystem to a Web Worker** — particles, the spatial hash, or replay decoding — with transferable buffers; measure main-thread time saved vs. message overhead; keep it only if it wins (and say so either way). **Load test**: a Node script spawning N headless WebSocket clients (`ws`) flying scripted paths; ramp N = 8, 32, 64, 128; record server tick-time p99, event-loop utilization, RSS, and bytes/s; find the N where tick time exceeds the 33 ms budget. Chart it in the README. That number is your **capacity**, and Lab 8 will make you defend it.

### Definition of done

- ≥ 60 Vitest tests incl. ≥ 5 fast-check properties; `shared/` coverage ≥ 85 %; Playwright two-browser e2e.
- CI green on push/PR with badge; lint (type-checked) clean.
- Before/after performance tables (frame p50/p95/p99, GC pauses, allocators, hot functions; server tick p99) with flame-chart screenshots; zero major GCs and p99 < 16.7 ms achieved (or a precise explanation of what limits your machine).
- Object pooling and allocation-free hot paths implemented where measurement justified them.
- Bots, a worker experiment with a go/no-go decision, and the load-test capacity chart.
- Repo tagged `lab-07`.

---

## Resources

**Watch**

- Franziska Hinkelmann — [JavaScript engines: how do they even? (JSConf EU 2017, 30 min)](https://www.youtube.com/watch?v=p-iiEDtpy6I). By a former V8 engineer: parsing, bytecode, JIT tiers, hidden classes, inline caches, deopts — the whole of Sections 1–2 in one talk, with humor.

**Read**

- Lydia Hallie — [JavaScript Visualized: the JavaScript Engine](https://dev.to/lydiahallie/javascript-visualized-the-javascript-engine-4cdf). The illustrated pipeline; read before the talk.
- Mathias Bynens & Benedikt Meurer — [JavaScript engine fundamentals: Shapes and Inline Caches](https://mathiasbynens.be/notes/shapes-ics). The definitive explanation of Section 2, with diagrams of shape transitions across engines. Read slowly.
- V8 team — [Trash talk: the Orinoco garbage collector](https://v8.dev/blog/trash-talk). Generational GC, scavenging, parallel/concurrent marking — and why pauses still happen.
- Robert Nystrom — [Game Programming Patterns: Object Pool](https://gameprogrammingpatterns.com/object-pool.html). The pattern, the free-list trick, and when *not* to pool.
- Chrome for Developers — [Analyze runtime performance](https://developer.chrome.com/docs/devtools/performance) and [Fix memory problems](https://developer.chrome.com/docs/devtools/memory-problems). Hands-on guides to the two panels you'll live in. Also web.dev's [RAIL model](https://web.dev/articles/rail) for the frame budgets.
- MDN — [Using Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers), [`OffscreenCanvas`](https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas), and [`Performance`](https://developer.mozilla.org/en-US/docs/Web/API/Performance) (mark/measure). Node: [`worker_threads`](https://nodejs.org/api/worker_threads.html).
- [Vitest](https://vitest.dev) (guide: getting started, mocking, fake timers, coverage), [fast-check](https://fast-check.dev) (introduction and "Why property-based?"), [Playwright](https://playwright.dev) (getting started, `webServer`, multiple contexts).
- [ESLint flat configuration](https://eslint.org/docs/latest/use/configure/configuration-files) with [typescript-eslint](https://typescript-eslint.io/), or [Biome](https://biomejs.dev). GitHub — [Building and testing Node.js](https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-nodejs).

---

## Deliverable checklist

- [ ] Root `npm test` runs Vitest in all packages; ≥ 60 tests; ≥ 5 fast-check properties (codec round-trip, length, garbage-safety, in-arena, parser accept/reject).
- [ ] Fake-timer tests for the accumulator loop and heartbeat; reconciliation tested as a pure function.
- [ ] `shared/` coverage ≥ 85 %.
- [ ] Playwright: two contexts, one room, movement observed cross-client, chat received.
- [ ] GitHub Actions: typecheck → lint → test → build → e2e; badge; lint with type-checked rules and `no-floating-promises`.
- [ ] `performance.mark/measure` instrumentation; before/after tables and flame-chart screenshots; zero major GCs in play; p99 frame < 16.7 ms.
- [ ] Pooling / allocation-free hot paths / shape fixes, each justified by a measurement.
- [ ] Server `--cpu-prof` analysis; tick p99 before/after; spatial hash if collision was the hot spot.
- [ ] Bots with the human input interface; worker experiment with measured go/no-go; load-test chart with the capacity N.
- [ ] Git tag `lab-07`.

---

## Reflection — explain it at the whiteboard

1. Draw V8's pipeline: parser → Ignition → (Maglev) → TurboFan. What triggers optimization? What triggers a deopt? Give an example from your code.
2. What is a hidden class / shape? Why is `obj.x` fast when a call site sees one shape and slow when it sees twenty? What does that mean for how you write constructors?
3. Explain generational GC. Why are young-generation collections cheap and old-generation ones expensive? Why does a *long-lived* particle cause more trouble than a short-lived one?
4. What did the profiler show as your top allocator, and what did you do about it? What's the downside of object pooling?
5. Why are typed arrays faster than arrays of objects for bulk numeric state? Name two things you lose.
6. Web Workers: three ways to move data across, with their costs. Why did your worker experiment win or lose?
7. Property-based test vs example test — when is each better? Show your codec round-trip property and explain shrinking.
8. Why is `no-floating-promises` important in a server? What bug does it prevent?
9. Your load test found capacity N. What was the bottleneck — CPU in the tick, bandwidth, or GC — and how do you know?

---

## Stretch

Move the **entire simulation** to a structure-of-arrays layout (`Float32Array` per field, integer entity handles, free-list allocation) and re-run every benchmark and every test — the tests should pass unchanged if your API held, which is the point of having them. Then try **`SharedArrayBuffer` + `Atomics`** to share the render state between the main thread and a simulation worker with no copying (set the COOP/COEP headers in Vite and on the server); measure frame time and input latency. Finally, run the server load test against **Node with `--jitless`** and under **Bun** or **Deno** — a small but real experiment in "how much of my performance is the engine?"
