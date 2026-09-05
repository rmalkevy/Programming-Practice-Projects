# Lab 04 — Node.js: The Other Runtime — `EventEmitter`, Streams, and a WebSocket Server

> "Node.js is the same language, a different world: no DOM, no window, and *everything* is I/O."

**Weeks:** 7–8 · **Language focus:** Node vs the browser, the Node event loop (libuv phases), CommonJS vs ESM, `EventEmitter`, streams and backpressure, `http`, `fs/promises`, `Buffer`, npm and `package.json`, environment config, the `ws` library · **Project step:** a game server with rooms, WebSocket join/leave/chat, and match logs streamed to disk · **Course:** [JavaScript — Build a Multiplayer Game](README.md) · **Previous:** [Lab 03](lab-03-async-javascript.md)

---

## This lab's feature

JavaScript's second home is the server. **Node.js** is V8 (the same engine as Chrome) plus **libuv** (a C library for asynchronous I/O) plus a standard library for files, networks, and processes — and no browser. Same language, same event loop *concept*, same promises; but a different set of globals, a different module history, and two foundational abstractions the browser doesn't have: **`EventEmitter`** and **streams**.

Every Node program is built on those two. HTTP servers emit `"request"`; sockets are duplex streams; files are readable streams; `process.stdout` is writable. Understanding **backpressure** — what happens when a fast producer feeds a slow consumer — is the single most important Node concept, and the one that separates servers that work from servers that fall over at load.

Your game needs a server. This lab builds it: a Node process that serves the client, manages rooms, and speaks **WebSocket** — the protocol that turns HTTP's request/response into a persistent two-way connection. By the end, two browser windows will see each other join a room and chat. The *game state* doesn't cross the wire yet — that's Lab 5, and it deserves its own two weeks.

---

## Theory

### 1. Node vs the browser

Same engine, different host. In Node: no `window`, `document`, `fetch`-until-recently (now built in), or `localStorage`; instead `process` (argv, env, exit, signals), `Buffer` (raw bytes — Node's pre-`Uint8Array` binary type, still everywhere), `require`/`import` of built-in modules (`node:fs`, `node:http`, `node:events`, `node:stream`), and direct access to the file system and network. `globalThis` is the global in both. The [official comparison](https://nodejs.org/en/learn/getting-started/differences-between-nodejs-and-the-browser) is short; read it.

**The Node event loop** is the same idea as the browser's, implemented by libuv with named **phases**: timers → pending callbacks → poll (I/O) → check (`setImmediate`) → close callbacks; with `process.nextTick` and promise microtasks drained between every phase. The practical rules: `setImmediate` runs after I/O callbacks in the current iteration; `setTimeout(fn, 0)` vs `setImmediate` ordering is nondeterministic from the main module but deterministic inside an I/O callback; `process.nextTick` runs *before* promise microtasks and can starve I/O if abused. The [official event loop guide](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) and Bert Belder's talk are the sources.

Node is still **single-threaded for your JavaScript**. libuv uses a thread pool for file I/O and DNS, but your code runs on one thread — so a 200 ms synchronous loop in a request handler stalls *every* connected client. Lab 1's lesson, with higher stakes. (`worker_threads` exist for CPU work; Lab 7.)

### 2. Modules: CommonJS vs ESM

Node predates ES modules and invented its own: **CommonJS** — `const x = require("./x")`, `module.exports = …`, synchronous, dynamically resolvable. Millions of packages use it. Modern Node supports **ESM** — `import`/`export`, the browser's system — when `package.json` has `"type": "module"` (or files end in `.mjs`). Rules for living in both worlds: **write ESM**; you can `import` CommonJS packages (their `module.exports` becomes the default export); CommonJS can `import()` ESM dynamically (and, since Node 22, can `require()` ESM in many cases); `__dirname` doesn't exist in ESM — use `import.meta.dirname` (Node 20.11+) or `fileURLToPath(import.meta.url)`. Prefix built-ins with `node:` (`import { readFile } from "node:fs/promises"`) so nobody confuses them with npm packages.

### 3. `EventEmitter`: the pattern under everything

```js
import { EventEmitter } from "node:events";
class Room extends EventEmitter {
  join(player) { this.players.add(player); this.emit("join", player); }
}
room.on("join", p => broadcast(`${p.name} joined`));
room.once("empty", () => rooms.delete(room.id));
```

`on`, `once`, `off`, `emit`. Listeners run **synchronously, in registration order**, on `emit`. It's Lab 3's `EventTarget` with a friendlier API and one crucial extra rule: **an `"error"` event with no listener throws** — crashing the process. Every emitter that can fail must have an `error` listener. `events.on(emitter, "name")` turns an emitter into an async iterator; `events.once` returns a promise. Node's HTTP server, sockets, streams, and `process` are all emitters; understand this class and you understand the shape of every Node API.

### 4. Streams and backpressure

A **stream** is an `EventEmitter` that moves data in chunks over time: **Readable** (a file, a request body, a socket's incoming side), **Writable** (a file, a response, a socket's outgoing side), **Duplex** (both — a socket), **Transform** (a duplex that modifies what passes through — gzip, a JSON-lines encoder). Chunks are `Buffer`s (or strings, or objects in *object mode*).

Why streams instead of reading everything into memory: a 2 GB match-log replay can't be `readFile`'d; a client on a slow connection can't absorb data as fast as you generate it. That second case is **backpressure**: `writable.write(chunk)` returns `false` when its internal buffer is above `highWaterMark`. If you ignore that and keep writing, the buffer grows without bound — memory climbs until the process dies. Correct behavior: stop producing until the `"drain"` event. Doing this by hand is error-prone; **`pipeline`** does it for you and propagates errors and cleanup:

```js
import { pipeline } from "node:stream/promises";
await pipeline(source, new JsonLinesTransform(), createWriteStream("match.ndjson"));
```

`for await (const chunk of readable)` is the async-iterator view (Lab 3), and `Readable.from(iterable)` turns any (async) iterable — including a generator — into a stream. The [official backpressure guide](https://nodejs.org/en/learn/modules/backpressuring-in-streams) is the best explanation of why this matters; the [stream API docs](https://nodejs.org/api/stream.html) are long but the "API for stream consumers" section is what you need.

A WebSocket connection is, under the hood, a duplex socket stream with framing on top — and a client that stops reading is exactly the slow consumer backpressure exists for. Lab 5 will make you care (`ws` exposes `socket.bufferedAmount` for this reason).

### 5. `http`, and serving the client

`http.createServer((req, res) => …)` is the raw server: `req` is a readable stream (method, url, headers, body chunks), `res` a writable one (`writeHead`, `write`, `end`). Serving static files properly — MIME types, caching headers, path traversal defense (`../../etc/passwd`) — is fiddly enough that you'll write it once to learn and then use `sirv` or Express/Fastify for real. A tiny JSON API (`GET /api/rooms`) needs URL parsing (`new URL(req.url, base)`), a body reader for POST (collect chunks; cap the size), and correct status codes. In development, Vite serves the client and **proxies** `/api` and `/ws` to your Node server (`server.proxy` in `vite.config.js`); in production Node serves the built `dist/`.

### 6. WebSockets: from request/response to a conversation

HTTP is client-asks, server-answers. A game needs the server to push state 20–60 times a second to every player. **WebSocket** ([RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)) starts as an HTTP request with `Upgrade: websocket`, then becomes a persistent, full-duplex, low-overhead connection carrying **messages** (text or binary frames) in both directions. Hussein Nasser's crash course covers the handshake and trade-offs in twenty minutes.

Server side, the [`ws`](https://github.com/websockets/ws) library: `new WebSocketServer({ server })` attaches to your HTTP server; `wss.on("connection", (socket, req) => …)`; `socket.on("message", data => …)`, `socket.send(data)`, `socket.on("close")`, `socket.on("error")` (**always**). Client side, the browser's built-in [`WebSocket`](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API): `new WebSocket("ws://…")`, `onopen`, `onmessage`, `send`, `close`, plus a reconnect-with-backoff wrapper you'll write (Lab 3's retry, again).

Design the **protocol** deliberately, even at v0: JSON messages with a `type` field (`{ type: "join", room, name }`, `{ type: "chat", text }`, `{ type: "roster", players: [...] }`), a version number, and a **schema you validate on the server** — never trust a client message's shape. Cap message size. Send heartbeats (`ping`/`pong` frames are built into the protocol; `ws` exposes them) to detect dead connections behind NATs and proxies. Lab 6 will type this protocol; Lab 5 will make part of it binary.

### 7. npm, `package.json`, and configuration

`package.json` is the manifest: `name`, `"type": "module"`, `scripts` (`dev`, `build`, `start`, `test`), `dependencies` vs `devDependencies`, `engines`. `package-lock.json` pins exact versions — **commit it**. Semver ranges (`^1.2.3` = compatible minor/patch) are what `npm install` resolves; `npm ci` installs exactly the lockfile. `npm run <script>` puts `node_modules/.bin` on `PATH`. Configuration comes from the environment (`process.env.PORT`), never from code — Node 20+ reads `.env` natively with `node --env-file=.env`; validate and default the values in one `config.js`. `node --watch server.js` restarts on change.

### Prove it to yourself (Node REPL / terminal, 15 minutes)

1. `node -e "setTimeout(()=>console.log('t'),0); setImmediate(()=>console.log('i')); process.nextTick(()=>console.log('n')); Promise.resolve().then(()=>console.log('p'))"` — run it five times. Which orders are stable and which aren't? Why?
2. `new EventEmitter().emit("error", new Error("boom"))` — what happened to the process? Add an `error` listener; repeat.
3. Write a `Readable.from(function* () { for (let i = 0; ; i++) yield Buffer.alloc(65536); }())` piped into a `Writable` whose `write` calls its callback after `setTimeout(…, 100)`. Watch `process.memoryUsage().rss` with `pipeline` vs. with a hand-rolled loop that ignores `write()`'s return value. Kill the second one before it kills your laptop.
4. `Buffer.from("привіт").length` vs `"привіт".length`. Explain. Then `Buffer.from([0xff, 0x00]).readUInt16BE(0)`.
5. A `WebSocketServer` and a `WebSocket` client in the same script; send a message and echo it. Then set `maxPayload: 1024` on the server and send 2 KB — what event fires where?

---

## Project step: the game server

### Set up the workspace

Split the repo into packages now (Lab 5 adds `shared/`):

```txt
dogfight/
  package.json               # "workspaces": ["client", "server"]
  client/                    # the Vite app from Labs 1–3 (moved here)
  server/
    package.json             # "type": "module"; deps: ws
    src/
      index.js               # http server + WebSocketServer + static/dist serving
      config.js              # PORT, HOST, LOG_DIR from env, validated
      rooms.js               # Room extends EventEmitter; RoomManager
      protocol.js            # message types, versions, validate(msg)
      ws.js                  # connection lifecycle, heartbeat, per-socket state
      log/
        matchlog.js          # Transform: events -> NDJSON; pipeline to disk
        replay.js            # Readable over an NDJSON file -> parsed events
    test/                    # a few node:test or vitest tests (formal suite in Lab 7)
```

### Milestones

**M1 — An HTTP server that serves the game and an API.**
`node:http` server (no framework yet — you're learning the layer) that serves `client/dist` in production with correct MIME types and a path-traversal guard, exposes `GET /api/rooms` (JSON list) and `POST /api/rooms` (create; body size capped; validated), and `GET /health`. Vite proxies `/api` and `/ws` in development. Config from `process.env` via `config.js`; `--env-file=.env` in dev. Graceful shutdown on `SIGINT`/`SIGTERM`: stop accepting, close sockets, flush logs, exit 0.

**M2 — Rooms and WebSocket lifecycle.**
`Room extends EventEmitter` (`join`, `leave`, `chat`, `empty` events; a `players` Map). `RoomManager` creates/finds/deletes rooms and deletes empty ones on `"empty"`. `ws.js`: on connection, expect a `join` message within 5 s or close; validate *every* message against `protocol.js` (unknown type, wrong shape, oversize → log and close with a code); attach `{ player, room }` to the socket; broadcast `roster` on join/leave and `chat` to the room; heartbeat with `ping` every 15 s and terminate sockets that miss two pongs; `"error"` listeners on *every* socket. Client: a `connection.js` wrapper with `onmessage` dispatch by `type`, a send queue while connecting, and reconnect with backoff — the lobby from Lab 3 now uses the real API and the real socket. *Check:* two browser windows join one room and see each other's names and chat.

**M3 — Match logs as streams.**
Every room owns a match log: an **object-mode `Transform`** that converts room events (`{ t, type, ...}`) into NDJSON lines, piped via `pipeline` to a `createWriteStream` under `LOG_DIR/<room>-<timestamp>.ndjson`. Feed it from the room's events (`Readable.from(events.on(room, "event"))` is one elegant route). Then `replay.js`: an async generator over `createReadStream` + a line splitter that yields parsed events — and a `GET /api/replays/:id` endpoint that **streams** the file to the client with `pipeline(readStream, res)`, never buffering it. Prove backpressure: generate a 200 MB synthetic log, download it through a bandwidth-throttled DevTools connection, and graph the server's `rss` over time (flat, if `pipeline` is doing its job). Put the graph in the README.

**M4 — Abuse handling and the event-loop write-up.**
Per-connection **rate limit** on messages (token bucket: N per second, then close), `maxPayload` on the server, a cap on players per room and rooms per server, and a **"slow client" policy**: if `socket.bufferedAmount` exceeds a threshold, drop that client's non-critical messages (or close it). Then a README section — one page — explaining: the Node event loop phases and how your server would behave if a handler blocked for 300 ms (demonstrate it with a deliberate busy-loop on `/api/slow` while another client chats); what backpressure is and where it showed up in M3; and why an unhandled `"error"` event or unhandled rejection takes the whole server down (demonstrate with a log excerpt, then show the fix).

### Definition of done

- `node:http` server serving the built client + JSON API + `/health`; env-based config; graceful shutdown.
- Rooms via `EventEmitter`; validated JSON protocol v0; heartbeats; two windows can join and chat.
- Client `connection.js` with reconnect/backoff and a send queue.
- Match logs via an object-mode `Transform` + `pipeline`; streaming replay endpoint; the flat-`rss` backpressure graph.
- Rate limiting, payload caps, slow-client policy; the event-loop/backpressure write-up with the blocking demonstration.
- Repo tagged `lab-04`.

---

## Deliverable checklist

- [ ] npm workspaces: `client/`, `server/`; `"type": "module"`; `node:`-prefixed built-ins.
- [ ] `node:http` static serving (MIME, traversal guard), `GET/POST /api/rooms`, `GET /health`; Vite proxy in dev.
- [ ] `config.js` from env with validation; `--env-file`; graceful `SIGTERM` shutdown.
- [ ] `Room extends EventEmitter`; `RoomManager`; roster/chat broadcast; join timeout.
- [ ] `protocol.js` with versioned, validated JSON messages; unknown/oversize → close with code.
- [ ] Heartbeat ping/pong; `"error"` listener on every socket; client reconnect with backoff + send queue.
- [ ] Object-mode `Transform` → NDJSON via `pipeline`; streaming replay endpoint; `rss`-over-time graph under throttled download.
- [ ] Token-bucket rate limit, `maxPayload`, room/player caps, `bufferedAmount` slow-client policy.
- [ ] Event-loop + backpressure write-up with the blocking demonstration and the crash-and-fix excerpt.
- [ ] Git tag `lab-04`.

---

## Reflection — explain it at the whiteboard

1. Draw the Node event loop phases. Where do `setTimeout`, `setImmediate`, `process.nextTick`, and promise reactions run? Why is `setTimeout(0)` vs `setImmediate` order unstable from the main module?
2. Node is single-threaded — so how does it read a file without blocking? What does libuv's thread pool handle, and what does it not?
3. CommonJS vs ESM: three differences. What is `import.meta.dirname` replacing?
4. What is backpressure? Show what `write()` returning `false` means and what happens if you ignore it. How does `pipeline` handle it?
5. What's the difference between a Readable, Writable, Duplex, and Transform? Which one is a TCP socket?
6. Walk through the WebSocket handshake. Why does a game use WebSockets rather than polling or SSE?
7. Why must every `EventEmitter` that can fail have an `"error"` listener? What happens otherwise, and what's the equivalent failure for promises in Node?
8. A client is on a 2G connection and your server sends 30 snapshots/s. What happens in the server's memory, how do you detect it, and what are your options?
9. Why validate every incoming message's shape on the server even though you wrote the client?

---

## Stretch

Replace the JSON match log with a **gzip-compressed** one (`zlib.createGzip()` in the pipeline) and measure size and CPU; then build a **live spectator** endpoint that streams a room's events *as they happen* (`Readable.from(events.on(room, "event"))` piped to the response, with SSE framing) — a second consumer of the same stream, which is the real test of your event design. Finally, port `index.js` to **Fastify** and note precisely what it added and what it hid.

---

## Resources

**Watch**

- Bert Belder — [Everything You Need to Know About Node.js Event Loop (Node Interactive 2016, 25 min)](https://www.youtube.com/watch?v=PNa9OMajw9w). By a libuv maintainer: the phases, the diagram everyone copies, and the corrections to the myths. Section 1.
- Hussein Nasser — [WebSockets Crash Course: Handshake, Use-cases, Pros & Cons (20 min)](https://www.youtube.com/watch?v=2Nt-ZrNP22A). The upgrade handshake, framing, and when WebSockets are the wrong tool. Section 6.
- Fireship — [Node.js Ultimate Beginner's Guide in 7 Easy Steps (16 min)](https://www.youtube.com/watch?v=ENrzD9HAZK4). A fast, accurate orientation to the runtime, modules, npm, and events if Node is new to you. Watch first, then the two above.

**Read**

- Node.js — [Differences between Node.js and the browser](https://nodejs.org/en/learn/getting-started/differences-between-nodejs-and-the-browser) and [The Node.js event loop, timers, and `process.nextTick()`](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick). The official guides; short and precise.
- Node.js — [Backpressuring in streams](https://nodejs.org/en/learn/modules/backpressuring-in-streams). The best single explanation of why streams exist. Read before M3.
- Node.js API — [`stream`](https://nodejs.org/api/stream.html) ("API for stream consumers" and "Implementing a transform stream"), [`events`](https://nodejs.org/api/events.html), [`process` signal events](https://nodejs.org/api/process.html#signal-events) for graceful shutdown.
- [`ws` — README and docs](https://github.com/websockets/ws). Server API, `maxPayload`, ping/pong, `bufferedAmount`. And MDN's [WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) for the client.
- [RFC 6455 — The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455). Read §1 (Introduction) and §5 (Data Framing). You'll understand what `ws` is hiding — and you'll need it for Lab 5's binary frames.
- npm — [`package.json` reference](https://docs.npmjs.com/cli/v10/configuring-npm/package-json) and [workspaces](https://docs.npmjs.com/cli/v10/using-npm/workspaces).
