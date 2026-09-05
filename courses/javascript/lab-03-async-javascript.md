# Lab 03 — Asynchronous JavaScript: Promises, `async`/`await`, and the Loading Screen

> "A promise is a placeholder for a value you don't have yet, plus a contract about how you'll be told."

**Weeks:** 5–6 · **Language focus:** callbacks → Promises → `async`/`await`; the three promise states; chaining and error propagation; microtask ordering; `Promise.all`/`allSettled`/`race`/`any`; `fetch` and `AbortController`; `EventTarget`; async iteration; Web Audio · **Project step:** an asset pipeline with a loading screen, a lobby over HTTP, sound effects · **Course:** [JavaScript — Build a Multiplayer Game](README.md) · **Previous:** [Lab 02](lab-02-objects-prototypes-classes.md)

---

## This lab's feature

Everything in Lab 1 and 2 was synchronous: the loop runs, the state updates, the frame paints. But a real game must *wait* — for sprite sheets to download, for audio to decode, for a server to answer "which rooms are open," for a player to click "Ready." And Lab 1 taught you the rule: you may never block the thread while waiting.

JavaScript's answer has evolved through three generations — callbacks (and callback hell), **Promises** (2015), and **`async`/`await`** (2017) — and all three are still in the code you'll read. Understanding them as *one* mechanism — promise reactions are microtasks; `await` is a suspension that resumes as a microtask — is what lets you predict execution order, handle errors without losing them, cancel things, and write concurrent code that stays readable. It's also the second half of the event-loop story you started in Lab 1, and the direct preparation for Node (Lab 4), where *everything* is asynchronous.

---

## Theory

### 1. Callbacks, and what went wrong

The original model: pass a function to be called later. `img.onload = () => …`, `setTimeout(fn, ms)`, `fs.readFile(path, (err, data) => …)`. It works, and it's still how the platform delivers events. Its failures at scale are well known: **nesting** (load A, then B, then C → the pyramid of doom), **error handling** (every callback checks `err`; forget once and the error vanishes), **inversion of control** (you hand your continuation to someone else's code and trust it to call you exactly once), and **no composition** (there's no callback-native way to say "wait for all of these").

### 2. Promises: a value with a state machine

A **Promise** is an object in one of three states — *pending*, *fulfilled* (with a value), or *rejected* (with a reason) — that transitions at most once. You attach reactions with `.then(onFulfilled, onRejected)`, `.catch`, and `.finally`. Two properties make promises composable:

- **`.then` returns a new promise**, resolved with the return value of the handler — so chains flatten: `load(a).then(() => load(b)).then(() => load(c))`. Return a promise from a handler and the chain *waits* for it (promise assimilation).
- **Rejections propagate** down the chain until something catches them. A thrown exception inside a handler becomes a rejection. One `.catch` at the end handles any failure along the way — the sane version of the `err` check.

Rules you must internalize: reactions **always run asynchronously** — as microtasks — even if the promise is already settled (`Promise.resolve(1).then(log); log(2)` prints `2, 1`). A promise settles **once**; later `resolve` calls are ignored. An unhandled rejection surfaces as an `unhandledrejection` event in browsers and (by default) crashes a Node process — never leave one dangling. And **never nest** `.then` inside `.then`; return instead.

Wrapping a callback API is the one time you construct a promise by hand:

```js
const loadImage = src => new Promise((resolve, reject) => {
  const img = new Image();
  img.onload  = () => resolve(img);
  img.onerror = () => reject(new Error(`failed to load ${src}`));
  img.src = src;
});
```

### 3. `async`/`await`: promises with sequential syntax

`async function f()` always returns a promise. Inside it, `await p` **suspends the function** until `p` settles, then resumes with the value (or throws the rejection reason). The suspension is not blocking: the function returns to the event loop at the `await`, and the continuation is scheduled as a **microtask** when `p` settles. `try/catch` works across `await`. This is the same "resumable function" idea as generators (Lab 2's `function*`), and `async/await` was in fact modeled on them.

Lydia Hallie's promise-execution video traces this frame by frame. The ordering puzzle, extended:

```js
async function a() { console.log(1); await null; console.log(2); }
a(); console.log(3);
// 1, 3, 2   — `await` yields even when awaiting a non-promise
```

The performance trap: **sequential `await` where you meant concurrent**. `const a = await loadA(); const b = await loadB();` loads B only after A finishes. Start both, then await both: `const [a, b] = await Promise.all([loadA(), loadB()]);`. This single mistake accounts for most "why is my app slow" async bugs.

### 4. Combinators: waiting for many

- **`Promise.all(ps)`** — fulfills with an array when *all* fulfill; rejects **immediately** when *any* rejects (the others keep running — there's no cancellation built in). Your asset loader.
- **`Promise.allSettled(ps)`** — waits for all, gives you `{status, value|reason}` for each. When partial failure is acceptable (a missing sound shouldn't block the game).
- **`Promise.race(ps)`** — settles with the *first* to settle, fulfilled or rejected. Timeouts: `race([fetch(url), rejectAfter(5000)])`.
- **`Promise.any(ps)`** — first to *fulfill*; rejects with an `AggregateError` only if all reject. Fastest-of-several-mirrors.

Progress for a loading screen: `Promise.all` gives you nothing until the end. Wrap each promise with `.then(v => { done++; onProgress(done / total); return v; })` before passing it to `all` — a pattern worth knowing.

### 5. `fetch`, `AbortController`, and cancellation

`fetch(url, options)` returns a promise for a `Response` — which resolves **as soon as headers arrive**, and *does not reject on HTTP errors* (a 404 is a fulfilled promise with `response.ok === false`; only network failures reject). Then `await response.json()` (or `.text()`, `.arrayBuffer()`, `.blob()`) reads the body — a second async step. Check `ok` every time; write a `fetchJson(url)` helper that throws on `!ok` and use only that.

Promises have no built-in cancellation. The platform's answer is **`AbortController`**: create one, pass `controller.signal` to `fetch` (and to `addEventListener`, and to your own async functions), call `controller.abort()` to reject everything listening with an `AbortError`. `AbortSignal.timeout(ms)` gives you a pre-armed signal — the correct way to time out a request. Design your own long-running async functions to accept a `signal` and check `signal.aborted` / listen for `"abort"`; a player who leaves the lobby should cancel the in-flight room fetch.

Retry with **exponential backoff and jitter** for transient failures (5xx, network errors) — never for 4xx. You'll write this once here and reuse it on the server in Lab 4.

### 6. Events, `EventTarget`, and decoupling

The DOM's event system is available to *your* objects: `class Lobby extends EventTarget` (or compose one), `this.dispatchEvent(new CustomEvent("roomsChanged", { detail: rooms }))`, `lobby.addEventListener("roomsChanged", e => render(e.detail))`. It's the browser-native observer pattern — the same one Node calls `EventEmitter` (Lab 4). Use it to decouple the lobby's data layer from its DOM rendering, and the game from its audio: the sim dispatches `"explosion"`; the audio module listens. The sim never imports the audio module.

Events and promises complement each other: **a promise is for a value that arrives once; an event is for things that happen repeatedly.** Convert between them when useful — `new Promise(r => target.addEventListener("ready", r, { once: true }))` awaits a single event.

### 7. Async iteration and streams

`for await (const chunk of asyncIterable)` iterates an **async iterator** — `next()` returns a promise. `async function*` generators produce them. `response.body` is a `ReadableStream` (also async-iterable in modern browsers) that lets you process a large download as it arrives — a progress bar with real bytes, or a level file parsed while streaming. This is Node's streams model (Lab 4) arriving in the browser; meet it here so Lab 4 feels familiar.

### 8. Web Audio, briefly

The [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) is async at every step: `fetch` the file, `await response.arrayBuffer()`, `await audioContext.decodeAudioData(buffer)` → an `AudioBuffer` you can play many times with zero latency via `AudioBufferSourceNode`. Two platform rules: an `AudioContext` can only start after a **user gesture** (click "Play"), and decoding is real work — do it during the loading screen, not on first fire. A `<audio>` element is simpler but has latency and can't overlap playback; games use Web Audio.

### Prove it to yourself (console, 15 minutes)

1. `Promise.resolve(1).then(console.log); console.log(2)` → order? Now the `1, 3, 2` async puzzle from Section 3. Then add a `setTimeout(() => console.log(4), 0)` at the top and predict the full order.
2. `fetch("https://httpbin.org/status/404").then(r => console.log(r.ok, r.status))` — it *fulfilled*. Now fetch a nonexistent host — this one rejects. State the rule.
3. Two `await`s of 1-second timers sequentially vs. via `Promise.all`. Time both with `performance.now()`.
4. `const c = new AbortController(); fetch("https://httpbin.org/delay/5", { signal: c.signal }).catch(e => console.log(e.name)); c.abort()` → what's `e.name`? Now with `AbortSignal.timeout(1000)` instead.
5. Create a rejected promise with no `.catch`. Watch the console. Now add `window.addEventListener("unhandledrejection", e => …)`. Then in Node (Lab 4 preview): `node -e "Promise.reject(new Error('x'))"` — what's the exit code?

---

## Project step: loading, lobby, and sound

### Milestones

**M1 — The asset pipeline and loading screen.**
`assets/manifest.json` lists sprites, sounds, and an arena definition. `src/assets/loader.js`: `loadImage`, `loadAudio(ctx, url)`, `loadJson` (via a shared `fetchJson` that checks `ok`), each accepting an `AbortSignal`, wrapped in a `withRetry(fn, { attempts, baseMs, signal })` with exponential backoff + jitter that never retries 4xx. `loadAll(manifest, { onProgress, signal })` uses `Promise.all` with per-item progress (Section 4). A **loading screen** on the canvas shows a real progress bar; the game starts only after `await loadAll(...)`. Deliberately add a nonexistent sprite and a slow one (Vite lets you add a delay in a dev-server middleware, or use `httpbin.org/delay`) to test failure and progress. *Check:* replace `Promise.all` with sequential `await`s in a branch and time the difference on the README.

**M2 — Sprites and sound in the game.**
Ships, bullets, and asteroids draw from loaded sprite sheets (`drawImage` with source rectangles). Sound: an `audio.js` module owning the `AudioContext`, unlocked on the first click, playing decoded buffers for shoot/hit/explosion. **The sim must not import `audio.js`**: the `World` (or a small `EventTarget`-based bus) dispatches `CustomEvent`s — `"fired"`, `"hit"`, `"exploded"` — and the audio module subscribes. Same for a `hud.js` that shows score changes.

**M3 — The lobby over HTTP.**
A lobby screen before the game: fetch `/api/rooms` (for now, a static `public/api/rooms.json` served by Vite, or a 30-line Node `http` server if you're eager — Lab 4 replaces it either way), render the list, let the player pick a name and a room, and "Join" (which, for now, starts a local game with that room's arena config). The lobby is a `class Lobby extends EventTarget` with `refresh()`, `join(roomId)`, and events; the DOM rendering is a separate module that listens. `refresh()` on an interval *while* the lobby is visible, cancelled via `AbortController` the moment the player leaves — no orphaned requests. A timeout on every request via `AbortSignal.timeout`.

**M4 — Ordering puzzles and a failure gallery.**
In the README: (a) five microtask/task ordering puzzles you wrote yourself, with the output and a one-line explanation each — at least one involving `await`, one involving `setTimeout` inside a `.then`, and one involving `requestAnimationFrame`; (b) a **failure gallery**: screenshots or logs of your loading screen handling a 404 sprite, a network timeout, an abort mid-load, and a corrupt JSON — each recovered gracefully (the game still starts, or the user sees a clear retry button). This is what "handles errors" means.

### Definition of done

- Assets load concurrently with real progress; failures and aborts are handled; retry with backoff is used and tested.
- The sim never imports audio or HUD modules; events decouple them.
- Sound plays via Web Audio after a user gesture; sprites render.
- A lobby fetches rooms with timeouts, periodic refresh, and abort-on-leave; `EventTarget`-based; rendering separated.
- Five ordering puzzles and the failure gallery are in the README.
- Repo tagged `lab-03`.

---

## Deliverable checklist

- [ ] `loadImage` / `loadAudio` / `loadJson` with `AbortSignal` support; `fetchJson` checks `ok`; `withRetry` with backoff + jitter, no retry on 4xx.
- [ ] `loadAll` via `Promise.all` with per-item progress; loading screen with a real bar; sequential-vs-concurrent timing in README.
- [ ] Sprite rendering from sheets; Web Audio module unlocked by user gesture; decoded during loading.
- [ ] `EventTarget`/`CustomEvent` bus; sim has zero imports of audio/HUD.
- [ ] Lobby (`extends EventTarget`) with periodic refresh, `AbortSignal.timeout`, abort-on-leave; rendering in a separate module.
- [ ] Five self-written ordering puzzles with explanations; failure gallery (404, timeout, abort, bad JSON).
- [ ] Git tag `lab-03`.

---

## Reflection — explain it at the whiteboard

1. The three promise states and the transitions. Why does `.then` on an already-fulfilled promise still run asynchronously, and as which kind of task?
2. Desugar `async function f() { const a = await g(); return a + 1; }` into `.then` calls. Where exactly does the function return control to the event loop?
3. Predict: `setTimeout(log1); Promise.resolve().then(log2).then(log3); (async () => { log4; await 0; log5 })(); log6`. Explain every position.
4. `Promise.all` vs `allSettled` vs `race` vs `any` — one use case each from your game. What happens to the *other* promises when `all` rejects?
5. Why doesn't `fetch` reject on a 404? What's the two-step nature of reading a response, and why?
6. How does `AbortController` implement cancellation without the promise having a cancel method? How do you make *your own* async function cancellable?
7. Promise vs event: when is each the right tool? Show converting one into the other.
8. What happens to an unhandled rejection in the browser? In Node? Why is that difference deliberate?

---

## Stretch

Stream the largest asset with `response.body` and `for await`, reporting **real byte-level progress** from `Content-Length`. Then implement a **priority loader**: critical assets (ship, arena) load first and the game becomes playable while decorative assets (music, particle sprites) continue in the background — an `async` generator yielding assets as they land, consumed by a `for await` that swaps placeholders. Finally, write **`Promise.all` from scratch** (using only `new Promise` and `.then`), then `allSettled`, and test them against the built-ins — the fastest way to prove you understand the state machine.

---

## Resources

**Watch**

- Lydia Hallie — [JavaScript Visualized: Promise Execution (13 min)](https://www.youtube.com/watch?v=Xs1EMmBLpn4). Frame-by-frame animation of `.then`, `await`, and the microtask queue. Watch before Section 3; it makes the ordering puzzles obvious.
- Fun Fun Function — [Promises (Functional Programming in JavaScript, 20 min)](https://www.youtube.com/watch?v=2d7s3spWAzo). Promises built up from the callback problem, live-coded. Older but exactly right about *why*.
- Jake Archibald — [In the Loop (JSConf.Asia 2018)](https://www.youtube.com/watch?v=cCOL7MC4Pl0) — rewatch the microtask section now that you're writing promise code.

**Read**

- javascript.info — [Promises, async/await](https://javascript.info/async) — all seven articles, especially "Promises chaining," "Error handling with promises," "Microtasks," and "Async/await." The textbook for this lab.
- MDN — [Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises) (the guide) and [`AbortController`](https://developer.mozilla.org/en-US/docs/Web/API/AbortController).
- Jake Archibald — [Tasks, microtasks, queues and schedules](https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/) — the "promises" section, now that you can read it fluently.
- Lydia Hallie — [JavaScript Visualized: Promises & Async/Await](https://dev.to/lydiahallie/javascript-visualized-promises-async-await-5gke). The article version, with diagrams you can pause on.
- Kyle Simpson — [*You Don't Know JS: Async & Performance* (1st ed.)](https://github.com/getify/You-Dont-Know-JS/blob/1st-ed/async%20%26%20performance/README.md). Chapters 2 ("Callbacks") and 3 ("Promises") explain *why* promises are designed the way they are — trust, inversion of control, and the "once" guarantee. The deepest treatment available.
- MDN — [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) — "Using the Web Audio API" and "Advanced techniques" for decoding and playback.
