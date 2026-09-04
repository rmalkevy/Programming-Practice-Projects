# Lab 05 — Real-Time Networking: Authoritative Server, Prediction, and Binary Protocols

> "The client is in the hands of the enemy."
> — every multiplayer programmer, eventually

**Weeks:** 9–10 · **Language focus:** `ArrayBuffer`, `DataView`, typed arrays, endianness, `TextEncoder`; sharing simulation code between client and server via workspaces; precise timers in Node; `structuredClone` · **Networking:** the authoritative server model, tick rates, snapshots, client-side prediction and server reconciliation, entity interpolation, latency simulation · **Project step:** two players dogfighting across the internet, smoothly, at 30 Hz, with a binary protocol · **Course:** [JavaScript — Build a Multiplayer Game](README.md) · **Previous:** [Lab 04](lab-04-node-streams-websockets.md)

---

## This lab's feature

This is the lab the course is named for. Two browsers, one server, and the hardest problem in game programming: **making it feel instant when the truth is 80 ms away.**

The naive design — each client runs its own simulation and tells the others where it is — fails twice: players see different games (floating-point drift, dropped packets), and anyone can teleport by editing a number in DevTools. The design every real-time game uses is the **authoritative server**: clients send *inputs*, the server runs the *one true simulation* and broadcasts *snapshots*. That fixes cheating and consistency and introduces the real problem: with 80 ms round-trip, your ship responds 80 ms after you press the key. Unplayable.

The fix — **client-side prediction with server reconciliation**, plus **interpolation** for other players — is a beautiful piece of engineering that Gabriel Gambetta explains in four short articles and that Overwatch's engineers explain in a GDC talk. You'll implement it. And because 30 snapshots a second of JSON is a bandwidth bill, you'll design a **binary protocol** with `DataView` — meeting JavaScript's raw-memory types, which you'll use again in Lab 7 for performance.

---

## Theory

### 1. The authoritative server model

Three roles for the same simulation code (which is why it must be **shared**, Section 5):

- **Server**: the only authority. Runs the simulation at a fixed **tick rate** (20–60 Hz; you'll use 30). Each tick: apply every input received since last tick, `world.step(dt)`, and broadcast a **snapshot** (the state of every entity, plus the tick number) to each client.
- **Client**: sends **inputs, never positions** — `{ seq, tick, thrust, turn, fire }` — every simulation step. Renders the world it *believes* in, which is a blend of what the server said and what it predicts.
- **Protocol**: inputs up, snapshots down, plus events that don't fit in state (a player joined, a sound to play).

The server must **validate inputs** (a `turn` of `1000` is a cheat) and can **rate-limit** them (Lab 4's token bucket). It never trusts a client's opinion of where anything is. Fiedler's [What Every Programmer Needs to Know About Game Networking](https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/) is the history of how the industry arrived here; Valve's [Source Multiplayer Networking](https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking) is the production reference.

### 2. Client-side prediction

Without prediction, your ship moves only when a snapshot arrives — one round-trip after the key press. **Prediction**: the client applies its *own* inputs to its *own* ship *immediately*, using the same `integrate` function the server uses. The ship responds instantly. Everyone else's ship still comes from snapshots.

This works because the simulation is **deterministic** (Lab 1): given the same state and inputs, the client and server compute the same result. Bugs that break determinism — `Math.random()` in the sim, iterating a `Map` whose insertion order differs, `Date.now()` — now become visible as the predicted ship diverging from the server's.

### 3. Server reconciliation

The server's snapshot for tick 100 arrives when the client is already predicting tick 104. If the client just snaps its ship to the snapshot, it jumps *backwards* four ticks — rubber-banding. **Reconciliation** (Gambetta part 2):

1. Every input the client sends carries a **sequence number**; the client keeps a buffer of unacknowledged inputs.
2. Each snapshot includes the **last input `seq` the server processed** for this client.
3. On receiving a snapshot: set the ship to the server's authoritative state, **discard inputs ≤ acknowledged seq**, then **re-apply** every remaining buffered input in order. Now the client's ship is where the server *will* say it is once those inputs arrive.

If prediction was correct, the result is pixel-identical and nothing visible happens. If the server disagreed (a collision the client didn't predict, a hit), the ship corrects — and a small **smoothing** (blend the visual position toward the reconciled one over a few frames) hides the snap. The Overwatch talk shows exactly this, at scale.

### 4. Entity interpolation

Other players' ships arrive as 30 discrete positions per second, but you render at 60–144 Hz. Drawing them at the latest snapshot position gives 30 Hz stutter. **Interpolation** (Gambetta part 3): render other entities **in the past** — buffer snapshots, and at render time, draw each remote entity at the position interpolated between the two snapshots that bracket `now − interpolationDelay` (typically 2 snapshot intervals, ~66 ms at 30 Hz). The cost: you see others ~100 ms behind the truth. Every real game makes this trade; the alternative is jitter.

Consequence for hit detection: when you shoot at where you *see* an enemy, the server knows they're not there anymore. **Lag compensation** — the server rewinds to what the shooter saw — is Fiedler's [snapshot interpolation](https://gafferongames.com/post/snapshot_interpolation/) sequel and the Stretch of this lab.

### 5. Sharing the simulation: workspaces and pure modules

The same `integrate`, `World.step`, collision, and protocol code must run in both runtimes. Create a **third workspace package**, `shared/`, imported by both `client/` and `server/` (`"shared": "workspace:*"` or a relative `file:` dependency; npm links it into `node_modules`). Rules that make this possible — and that you've been following since Lab 1:

- The sim has **no DOM, no canvas, no Node built-ins**: only language features. Check with a test that imports it in Node.
- **Deterministic**: no `Math.random()` — use a seeded PRNG (`mulberry32`) whose seed the server sends; no `Date.now()`; step with a fixed `dt`.
- **Serializable**: state is plain data (numbers, arrays, plain objects, or typed arrays), so it can be snapshotted with `structuredClone` and encoded with `DataView`. Class instances must be reconstructable from data — a `static fromSnapshot` on each entity kind.

The server's tick loop uses a **precise timer**: `setInterval(tick, 33)` drifts and coalesces; instead schedule each tick with `setTimeout` against an absolute target time (`nextTick += 1000/30; setTimeout(tick, nextTick − performance.now())`), and measure actual tick duration and jitter (both go in your stats endpoint). If a tick takes longer than the interval, you're CPU-bound — the Lab 7 problem.

### 6. Binary data: `ArrayBuffer`, `DataView`, typed arrays

A JSON snapshot of 8 ships × 6 fields at 30 Hz is ~30 KB/s per client, with number-to-string conversion both ways. A **binary** encoding is 8 × 24 bytes = 192 bytes per snapshot — under 6 KB/s — and zero parsing. JavaScript's raw-memory types:

- **`ArrayBuffer`** — a fixed-length block of bytes. No methods to read it; you need a *view*.
- **Typed arrays** — `Uint8Array`, `Int16Array`, `Float32Array`, … — a view of a buffer as one element type, platform-endian. Fast bulk access; the wrong tool for *mixed* layouts.
- **`DataView`** — read/write any type at any byte offset **with explicit endianness**: `view.setFloat32(offset, x, true)` (little-endian), `view.getUint16(offset, true)`. This is your encoder/decoder.
- **`TextEncoder`/`TextDecoder`** — strings ↔ UTF-8 bytes, for names and chat.

Design the message layout as a **spec** in a comment before writing code: byte 0 = message type; bytes 1–4 = tick (`Uint32`); then per entity: id `Uint16`, kind `Uint8`, x/y `Float32`, angle as `Int16` in 1/1000 radians (quantization: 2 bytes instead of 4, no visible loss), … Pick **little-endian everywhere** and say so. Version the format. WebSockets carry binary frames natively: `socket.binaryType = "arraybuffer"` on the client; `ws` gives you a `Buffer` (which *is* a `Uint8Array`) on the server. MDN's [typed arrays guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Typed_arrays) and [`DataView`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView) reference cover the API; the discipline is yours.

Further compression — **delta snapshots** (send only what changed since the last acknowledged snapshot), quantization, bit-packing — is the Stretch. Measure before optimizing: log bytes/s per client for JSON vs binary first.

### 7. Simulating latency, and measuring

You cannot develop netcode on `localhost` with 0 ms latency; everything looks fine. Build a **latency injector** into the server's send and receive paths: an artificial delay (`setTimeout` before processing/sending) with configurable base + jitter, and a configurable **packet drop** rate — controlled by a query parameter or admin message so you can toggle it live. Then a **netgraph** overlay on the client: RTT (ping/pong timestamps), snapshot age, bytes in/out per second, unacknowledged input count, reconciliation correction magnitude. This overlay is your instrument for the whole lab; build it first.

### Prove it to yourself (console/Node, 15 minutes)

1. `const b = new ArrayBuffer(8); const v = new DataView(b); v.setFloat32(0, 1.5, true); new Uint8Array(b)` — read the bytes. Now `v.setFloat32(0, 1.5, false)` — the bytes reversed. That's endianness.
2. `new Uint16Array(new Uint8Array([1, 0, 0, 1]).buffer)` — what did you get, and why does it depend on your CPU?
3. `JSON.stringify` a snapshot of 8 ships and `new TextEncoder().encode(json).byteLength`. Encode the same with a `DataView` layout. Ratio?
4. `setInterval(() => times.push(performance.now()), 33)` for 5 s; compute the intervals. Then the absolute-target `setTimeout` version. Compare jitter.
5. Run your `integrate` for 1,000 steps on the same inputs in Chrome and in Node; hash the final state. Identical? Add `Math.random()` somewhere and repeat.

---

## Project step: two players, one truth

### Milestones

**M1 — Shared simulation, server tick, dumb client.**
Create `shared/` with `sim/` (moved from `client/`), a seeded PRNG, `protocol/` (message types), and `codec/` (Section 6, initially JSON). Server: a `Match` per room running `World.step` at 30 Hz with the precise timer; applies validated inputs; broadcasts snapshots (JSON for now) with `lastProcessedSeq` per client. Client: sends inputs each sim step with `seq`; **no prediction yet** — the ship moves only on snapshots. Build the latency injector and the netgraph. *Check:* with 100 ms injected latency, feel exactly how bad it is; record the netgraph.

**M2 — Prediction and reconciliation.**
Client predicts its own ship with the shared `integrate`; keeps the pending-input buffer; on snapshot, reconcile (Section 3) and re-apply; smooth corrections over ~100 ms. Log the correction magnitude per snapshot to the netgraph. *Check:* at 100 ms latency, your ship feels instant; corrections read ~0 in open space and spike on collisions. Then break determinism on purpose (`Math.random()` in `integrate`) and watch the corrections grow — screenshot it for the README, then fix it.

**M3 — Interpolation, and the second player.**
Remote entities are buffered and rendered `interpolationDelay` in the past (Section 4), with the delay shown in the netgraph and adjustable live. Handle entities appearing/disappearing between snapshots. Bullets: predict your own locally (spawn immediately; the server's authoritative bullet replaces it by id), interpolate others'. *Check:* two browser windows (or two machines) dogfight smoothly at 100 ms ± 30 ms jitter with 2% drop. Record a 20-second GIF of both windows side by side — this goes at the top of your README for the rest of the course.

**M4 — Binary protocol and the measurements.**
Implement the `DataView` codec for inputs and snapshots per your written spec (little-endian, versioned, quantized angle); switch `binaryType`; keep the JSON codec behind a flag for comparison. Round-trip tests: `decode(encode(msg))` deep-equals `msg` within quantization tolerance (Lab 7 turns these into property tests). Then the README table, at 30 Hz with 4 players:

| Codec | Bytes/snapshot | KB/s per client (down) | KB/s per client (up) | Encode+decode µs |
|---|---|---|---|---|
| JSON | | | | |
| Binary (`DataView`) | | | | |

Plus a **netcode write-up** (one page): the three problems (latency, consistency, cheating) and how the design addresses each; what your netgraph showed before/after prediction; what determinism bug you hit; the interpolation-delay trade-off you chose and why.

### Definition of done

- `shared/` package with a pure, deterministic, seeded simulation imported by both client and server; a Node test proves it imports without DOM.
- 30 Hz authoritative server with precise timing, input validation, and per-client `lastProcessedSeq`.
- Prediction + reconciliation + smoothing for the local ship; interpolation for remote entities; local bullet prediction.
- Latency/jitter/drop injector and a client netgraph with RTT, snapshot age, bytes/s, pending inputs, correction magnitude.
- Binary `DataView` protocol with a written spec and round-trip tests; JSON-vs-binary table.
- Two-player GIF at the top of the README; the netcode write-up.
- Repo tagged `lab-05`.

---

## Resources

**Watch**

- Timothy Ford / Blizzard — [Overwatch Gameplay Architecture and Netcode (GDC 2017, 60 min)](https://www.youtube.com/watch?v=W3aieHjyNvw). ECS architecture in the first half; prediction, reconciliation, and how it feels to the player in the second. The best netcode talk on the internet; watch the networking half before M2 and the whole thing when you're done.

**Read**

- Gabriel Gambetta — [Fast-Paced Multiplayer](https://www.gabrielgambetta.com/client-server-game-architecture.html) — all four parts plus the **live demo** on the last page, which lets you toggle prediction, reconciliation, and interpolation with latency sliders. This is the lab's spine; read it twice.
- Glenn Fiedler — [What Every Programmer Needs to Know About Game Networking](https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/) (history and the authoritative model) and [Snapshot Interpolation](https://gafferongames.com/post/snapshot_interpolation/) (the details of buffering and interpolating, with numbers).
- Valve — [Source Multiplayer Networking](https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking). How Counter-Strike does it: tick rates, interpolation delay, lag compensation — a production system described plainly.
- Paul Bettner & Mark Terrano — [1500 Archers on a 28.8: Network Programming in Age of Empires and Beyond](https://www.gamedeveloper.com/programming/1500-archers-on-a-28-8-network-programming-in-age-of-empires-and-beyond). The *other* architecture — deterministic lockstep — and why it wasn't chosen here. Know the alternative.
- MDN — [JavaScript typed arrays](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Typed_arrays) and [`DataView`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/DataView).
- npm — [Workspaces](https://docs.npmjs.com/cli/v10/using-npm/workspaces) for the `shared/` package setup.

---

## Deliverable checklist

- [ ] `shared/` workspace: sim, seeded PRNG, protocol, codec; imports cleanly in Node and browser; determinism test (same inputs → same hash on both).
- [ ] Server `Match` at 30 Hz with absolute-target timer; tick duration/jitter in `/api/stats`; input validation and rate limiting.
- [ ] Inputs carry `seq`; snapshots carry `tick` and `lastProcessedSeq`.
- [ ] Prediction, reconciliation with input replay, correction smoothing; determinism-break experiment documented.
- [ ] Interpolation buffer with adjustable delay; entity appear/disappear handled; local bullet prediction.
- [ ] Latency/jitter/drop injector; netgraph overlay.
- [ ] `DataView` codec per written spec; round-trip tests; JSON vs binary table.
- [ ] Two-player side-by-side GIF; one-page netcode write-up.
- [ ] Git tag `lab-05`.

---

## Reflection — explain it at the whiteboard

1. Why must the server be authoritative? Name the two problems a client-authoritative design has, with a concrete exploit for one of them.
2. Explain client-side prediction. What property of the simulation does it depend on, and how would you *detect* that property being violated?
3. Walk through reconciliation with a diagram: client at tick 104, snapshot for tick 100 arrives acknowledging `seq` 57, buffer holds `seq` 55–61. What happens, step by step?
4. Why interpolate remote entities *in the past*? What does the interpolation delay trade off, and what value did you choose?
5. What is lag compensation, and why does interpolation make it necessary?
6. `DataView` vs a `Float32Array` view — when is each right? Why does endianness matter for a protocol and not for a local typed array?
7. Your binary snapshot quantizes the angle to `Int16`. What's the precision, and how did you decide it was enough?
8. Why not `setInterval` for the server tick? What does the absolute-target scheme fix, and what happens when a tick overruns?
9. What would break if the sim used `Math.random()`? Iterated a `Set` of entities? Used `Date.now()`?

---

## Stretch

Implement **delta compression**: the server tracks the last snapshot each client acknowledged and sends only changed fields (a bitmask per entity), falling back to a full snapshot when the ack is too old — and measure the new bytes/s row. Then **lag compensation** for bullets: the server keeps a ring buffer of recent world states and evaluates each shot against the state the shooter *saw* (their reported interpolation time), per Valve's article. Finally, put the latency injector under **automated test**: a Node script spawning 4 headless clients that fly scripted paths for 60 s at 150 ms/5% drop and asserts the mean reconciliation correction stays under a threshold — your first netcode regression test, ready for Lab 7's CI.
