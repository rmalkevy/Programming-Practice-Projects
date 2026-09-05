# Lab 01 — The Event Loop Is the Game Loop

> "JavaScript is single-threaded, non-blocking, asynchronous, concurrent. Which is a lot of words that sound contradictory until you see the loop."
> — Philip Roberts, paraphrased

**Weeks:** 1–2 · **Language focus:** how JavaScript runs — call stack, heap, task queue, microtask queue, `requestAnimationFrame`; ES modules; `let`/`const`, block scope, and closures; the Canvas 2D API · **Project step:** a ship you fly on a canvas at 60 fps, driven by a fixed-timestep simulation · **Course:** [JavaScript — Build a Multiplayer Game](README.md)

---

## This lab's feature

JavaScript runs on **one thread**. There is no parallelism in your page's script; there's a single loop that pulls one piece of work at a time from a queue, runs it to completion, and goes back for the next. Every click handler, every `setTimeout` callback, every network response, every frame of your game — one at a time, in order, on that one thread.

This is either the most limiting or the most liberating fact about the language, depending on whether you understand it. Understand it and you'll know exactly why a `for` loop that runs for 200 ms freezes the whole page, why `setTimeout(fn, 0)` doesn't run immediately, why a promise callback beats a timer callback that was scheduled first, and why `requestAnimationFrame` exists. Misunderstand it and you'll spend your career fighting mysterious jank.

A game makes the loop *visible*. Your simulation must advance in fixed steps while the browser paints frames at whatever rate the display allows, and every millisecond you waste in a frame is a stutter the player feels. This lab builds that loop, correctly, and puts a ship on it.

---

## Theory

### 1. The runtime: call stack, heap, and one thread

The JavaScript engine (V8 in Chrome and Node) has a **heap** (where objects live) and a **call stack** (the frames of currently executing functions). It runs whatever is on the stack until the stack is empty. Nothing can interrupt a running function — no other JavaScript runs until it returns.

The engine itself has no concept of "later." `setTimeout`, DOM events, `fetch`, `requestAnimationFrame` — none of these are part of the JavaScript language. They are **Web APIs** provided by the browser (or Node's libuv), running in the host outside the engine. When they have something for you, they don't call your function; they put it in a **queue**.

### 2. The event loop, tasks, and microtasks

The **event loop** is the host's loop: *when the call stack is empty, take the next callback from a queue and push it onto the stack.* That's the whole algorithm. Philip Roberts's talk animates it; watch it before reading further.

There are two queues, and their priority is the source of most confusion:

- **Task queue** (macrotasks): `setTimeout`/`setInterval` callbacks, DOM events, message events, I/O. **One task per loop iteration**; the browser may render between tasks.
- **Microtask queue**: promise reactions (`.then`, `await` continuations), `queueMicrotask`, `MutationObserver`. **Drained completely** after every task and after every callback — before the browser gets a chance to render or run the next task. A microtask that queues another microtask runs in the same drain. An infinite microtask chain freezes the page exactly like an infinite loop.

The canonical puzzle:

```js
console.log("1");
setTimeout(() => console.log("2"), 0);
Promise.resolve().then(() => console.log("3"));
console.log("4");
// 1, 4, 3, 2
```

`1` and `4` are synchronous. The stack empties. Microtasks drain first: `3`. Then the next task: `2`. Jake Archibald's article walks through a dozen variants of this with diagrams; do the exercises in it until they're boring.

Consequences for the game: **anything you do on the main thread costs frame time**. A 20 ms JSON parse in a frame is a dropped frame at 60 fps (16.7 ms budget). Chrome DevTools' Performance panel shows you the loop iteration by iteration — you'll use it in Lab 7.

### 3. `requestAnimationFrame`: painting with the display, not against it

`setInterval(render, 16)` is the wrong way to animate: timers drift, they aren't aligned with the display's refresh, they keep running in background tabs, and 16 ≠ 16.667. **`requestAnimationFrame(cb)`** asks the browser to call `cb` *once, right before the next paint*, passing a high-resolution timestamp. Call it again inside `cb` and you have a loop synchronized to the display — 60 Hz on most screens, 120 or 144 on others, paused when the tab is hidden.

Where does rAF sit in the loop? After tasks and microtasks, when the browser decides to render: run rAF callbacks → style → layout → paint. It's neither a task nor a microtask; it's a **rendering step**. Jake Archibald's "In the Loop" talk places it precisely, including the surprising fact that `setTimeout(fn, 0)` inside a rAF callback runs *before* the next frame's rAF, not after the paint.

### 4. Fixed timestep: the simulation must not depend on frame rate

If you move the ship `velocity * 1` per frame, it moves twice as fast on a 120 Hz display. If you move it `velocity * dt` with the real elapsed time, physics becomes non-deterministic (different collisions on different machines — fatal for multiplayer, Lab 5) and explodes on a long frame (a 500 ms hitch teleports the ship through a wall).

Glenn Fiedler's ["Fix Your Timestep!"](https://gafferongames.com/post/fix_your_timestep/) is the canonical answer, and every game programmer knows it:

```js
const STEP = 1 / 60;          // simulation runs at exactly 60 Hz, always
let accumulator = 0, last = performance.now();

function frame(now) {
  accumulator += Math.min((now - last) / 1000, 0.25);   // clamp: never spiral after a hitch
  last = now;
  while (accumulator >= STEP) {       // catch up in fixed steps
    simulate(STEP);
    accumulator -= STEP;
  }
  render(accumulator / STEP);         // alpha in [0,1): interpolate between last two states
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

The simulation is **deterministic** (same inputs → same result, regardless of display) and the renderer **interpolates** between the previous and current state so motion looks smooth at any refresh rate. Two states per entity, one blend factor. Nystrom's [Game Loop](https://gameprogrammingpatterns.com/game-loop.html) chapter covers the same ground from a design-pattern angle.

### 5. ES modules: `import`, `export`, and what changed

`<script type="module" src="main.js">` turns on **ES modules (ESM)**: every file is its own scope (no accidental globals), strict mode is on, `import`/`export` link files statically (the browser can analyze the dependency graph before running anything), and modules are deferred by default — they run after the document has parsed. Top-level `await` works. `this` at module top level is `undefined`.

Rules that matter: **named exports** (`export function simulate()`) are preferable to default exports (they're refactor-safe and grep-able); imports are **live bindings**, not copies; module code runs **once**, however many files import it (so a module is a natural singleton — your input state, for example). In development Vite serves ESM natively; for production it bundles. The [MDN modules guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) covers the rest.

### 6. Scope, closures, and why `let`/`const` exist

`var` is function-scoped and hoisted (usable before its line, as `undefined`). `let` and `const` are **block-scoped** and have a **temporal dead zone** (referencing them before their line throws). Use `const` by default, `let` when you must reassign, `var` never. The classic bug `var` causes — every callback in a loop seeing the same `i` — is the classic demonstration of **closures**: a function retains access to the variables of the scope it was created in, *by reference*, for as long as it lives.

Closures are how you'll build the game loop's private state without classes (Lab 2 gives you classes; you'll find you often don't need them):

```js
export function createInput(target) {
  const down = new Set();                               // private: nobody outside can touch it
  target.addEventListener("keydown", e => down.add(e.code));
  target.addEventListener("keyup",   e => down.delete(e.code));
  return { isDown: code => down.has(code) };            // the closure is the API
}
```

Kyle Simpson's *Scope & Closures* is the deep treatment; the first three chapters are enough for now.

### 7. The Canvas 2D API in five calls

`canvas.getContext("2d")` gives you an immediate-mode drawing API: `clearRect`, `fillRect`, `beginPath`/`arc`/`lineTo`/`stroke`, `drawImage`, and the transform stack — `save()`, `translate(x, y)`, `rotate(angle)`, draw, `restore()`. Draw the ship at the origin pointing right; translate and rotate the *canvas* to place it. Handle **device pixel ratio**: set `canvas.width = cssWidth * devicePixelRatio` and `ctx.scale(dpr, dpr)`, or everything is blurry on a retina display. The [MDN canvas tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial) is the reference; you need the first four sections.

### Prove it to yourself (browser console, 10 minutes)

1. Run the `1, 4, 3, 2` puzzle. Then add `queueMicrotask(() => console.log("5"))` after the promise line and predict the output before running.
2. `setTimeout(() => console.log("timer"), 0); const t = Date.now(); while (Date.now() - t < 2000) {}; console.log("done")` — when does `timer` print? Why couldn't the browser run it earlier?
3. In a rAF loop, log `now - last` for 100 frames. Then open a second tab and come back. Then plug in / change to a 120 Hz display if you have one. What changed?
4. `for (var i = 0; i < 3; i++) setTimeout(() => console.log(i))` vs the same with `let`. Explain both outputs in terms of scope and closures.
5. A `<script type="module">` that does `console.log(this)`, and a classic `<script>` that does the same. Then try to read a top-level `const` from one module in another without `import`.

---

## Project step: a ship you can fly

### Set up the project

```bash
npm create vite@latest dogfight -- --template vanilla     # plain JS; TypeScript arrives in Lab 6
cd dogfight && npm install
npm install -D eslint prettier     # or: npm install -D @biomejs/biome
echo "22" > .nvmrc                  # or 24
git init && git add . && git commit -m "Lab 1: project skeleton"
```

Target layout at the end of this lab:

```txt
dogfight/
  index.html                 # a <canvas>, a <script type="module" src="/src/main.js">
  package.json               # "type": "module"
  src/
    main.js                  # wires everything; starts the loop
    loop.js                  # createLoop({ step, simulate, render }) — fixed timestep
    input.js                 # createInput(target) — closure over key state
    sim/
      ship.js                # ship state + integrate(ship, input, dt)
      arena.js               # bounds, wrap-around
    render/
      canvas.js              # DPR-aware canvas setup
      draw.js                # drawShip(ctx, ship), drawHud(ctx, stats)
  README.md
```

### Milestones

**M1 — The loop, with proof.**
`loop.js` exports `createLoop({ step = 1/60, simulate, render })` returning `{ start, stop }`, implemented with `requestAnimationFrame` and the accumulator pattern from Section 4 (clamped). It tracks and exposes: simulation steps per second, render frames per second, and the last frame's duration. `render` receives the interpolation `alpha`. Show all three numbers in a HUD. *Check:* steps/s reads 60 on every machine; frames/s reads your display's refresh rate.

**M2 — Input as a closure, ship as data.**
`input.js` as in Section 6 (plus `justPressed` for edge-triggered keys — think about how). `sim/ship.js`: a ship is a plain object `{ x, y, vx, vy, angle, thrust }`; `integrate(ship, input, dt)` applies rotation, thrust along the heading, drag, and speed clamp — pure function of state + input + dt, no rendering, no DOM. `arena.js` wraps the ship around the edges. The ship flies. Tune it until it feels good; write down what you changed and why.

**M3 — Render with interpolation, correctly.**
Keep `previous` and `current` ship states; `render(alpha)` draws at `lerp(previous, current, alpha)` (and handles angle wrap-around when lerping the heading — a classic bug). DPR-aware canvas that resizes with the window. Ship drawn via `translate`/`rotate`, a simple thrust flame when thrusting, a grid or starfield so motion is visible. *Check:* movement is glass-smooth at 60 and at 120 Hz, and `simulate` was called the same number of times on both.

**M4 — Break it on purpose, then measure.**
Three experiments, each with a screenshot or a number in the README:

1. Put a `while (performance.now() < t + 100) {}` busy-wait in `render` every 60th frame. Describe what the player sees and what the HUD numbers do. Remove it. Explain, with the event loop, why a 100 ms *synchronous* block can never be "worked around" from JavaScript on the same thread.
2. Replace `requestAnimationFrame` with `setInterval(frame, 16)`. Record frames/s and the frame-time jitter for 10 s. Switch to a background tab for 5 s and back. Restore rAF. Report what differed.
3. Remove the accumulator (variable timestep: `simulate(dt)` once per frame). Throttle the CPU 6× in DevTools. Show that the ship's trajectory now differs between throttled and unthrottled runs (log the position after 5 s of holding "thrust"). Restore the fixed step; show the positions now match.

### Definition of done

- A ship flies smoothly on a canvas with keyboard control; the HUD shows steps/s, frames/s, frame time.
- The simulation is fixed-step and deterministic; the renderer interpolates; DPR is handled.
- `loop.js`, `input.js`, and the sim are separate ESM modules with named exports; the sim has no DOM/canvas dependencies.
- The three experiments are documented in the README with numbers.
- ESLint/Prettier (or Biome) configured and clean; `.nvmrc` present.
- Repo tagged `lab-01`.

---

## Deliverable checklist

- [ ] Vite project, `"type": "module"`, ESLint/Prettier or Biome, `.nvmrc`.
- [ ] `createLoop` with rAF + clamped accumulator; exposes steps/s, frames/s, frame time; HUD shows them.
- [ ] `createInput` closure with `isDown` and `justPressed`.
- [ ] Pure `integrate(ship, input, dt)`; arena wrap-around; no DOM in `sim/`.
- [ ] Interpolated rendering with correct angle lerp; DPR-aware, resizable canvas.
- [ ] Experiments 1–3 documented with numbers/screenshots and event-loop explanations.
- [ ] Git tag `lab-01`.

---

## Reflection — explain it at the whiteboard

1. Draw the runtime: call stack, heap, Web APIs, task queue, microtask queue, render steps. Trace `setTimeout(f, 0); Promise.resolve().then(g);` through it.
2. Why does a 100 ms synchronous loop freeze the whole page, including CSS animations and scrolling in many cases? What *can't* JavaScript do about it from the same thread?
3. Microtasks vs tasks: state the rule for when each runs. Why can a microtask chain starve rendering while a `setTimeout` chain can't?
4. Where does `requestAnimationFrame` run relative to tasks, microtasks, and paint? Why is it better than `setInterval(fn, 16)` for animation — give three reasons.
5. Explain the accumulator loop. Why clamp the frame delta? What is `alpha` and what does the renderer do with it?
6. Why must the simulation be deterministic, and what does that have to do with multiplayer (Lab 5)?
7. What does a closure capture — values or variables? Show the `var`/`let` loop difference and explain it precisely.
8. What changes when you add `type="module"` to a script tag? Name five things.

---

## Stretch

Add **gamepad support** via the [Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API) (polled in the loop, not event-driven — think about why that fits the loop better) and **touch controls** for phones. Then build a tiny **frame-time histogram** overlay (a canvas strip showing the last 120 frame durations, red above 16.7 ms) — you've just written the first tool of Lab 7. Finally, make the simulation run in a **Web Worker** with the main thread only rendering: which of your modules move, which stay, and how does the interpolation change when state arrives by message?

---

## Resources

**Watch**

- Philip Roberts — [What the heck is the event loop anyway? (JSConf EU 2014, 27 min)](https://www.youtube.com/watch?v=8aGhZQkoFbQ). The most-watched JavaScript talk ever, deservedly: the call stack, Web APIs, the task queue, and a live visualizer. Watch this first, before anything else.
- Jake Archibald — [In the Loop (JSConf.Asia 2018, 35 min)](https://www.youtube.com/watch?v=cCOL7MC4Pl0). The sequel: where `requestAnimationFrame`, microtasks, and rendering sit in the loop, with animations. Section 3 comes from this talk.
- Lydia Hallie — [JavaScript Visualized: Event Loop, Web APIs, (Micro)task Queue (13 min)](https://www.youtube.com/watch?v=eiC58R16hb8). A crisp, modern, diagram-driven recap. Watch after the two above to consolidate.

**Read**

- Jake Archibald — [Tasks, microtasks, queues and schedules](https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/). The definitive written explanation, with an interactive step-through. Do the exercises.
- javascript.info — [Event loop: microtasks and macrotasks](https://javascript.info/event-loop). Concise and correct; a good second angle.
- MDN — [JavaScript execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Execution_model) (agents, the loop, run-to-completion) and [`requestAnimationFrame`](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame).
- Glenn Fiedler — [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/). The essay every game programmer has read. Ten minutes; Section 4 is a summary.
- Robert Nystrom — [Game Programming Patterns: Game Loop](https://gameprogrammingpatterns.com/game-loop.html) and MDN's [Anatomy of a video game](https://developer.mozilla.org/en-US/docs/Games/Anatomy). Same topic, two more angles.
- MDN — [JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) and the [Canvas tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial) (first four sections).
- Kyle Simpson — [*You Don't Know JS Yet: Scope & Closures*](https://github.com/getify/You-Dont-Know-JS/blob/2nd-ed/scope-closures/README.md), Chapters 1–3 and 7 ("Using Closures"). Free.
- [Vite — Getting Started](https://vite.dev/guide/). Ten minutes; you'll live in it all semester.
