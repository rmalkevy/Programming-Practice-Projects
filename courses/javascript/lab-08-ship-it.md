# Lab 08 — Ship It: Production Node, Docker, CI/CD, Observability, and the Finish

> "It's not done until strangers are using it."

**Weeks:** 15–16 · **Runtime / operations focus:** production Node (`NODE_ENV`, signals, health checks, keep-alive); WebSockets behind reverse proxies; Docker multi-stage builds for a monorepo; environment and secrets; TLS/WSS; origin checks, rate limits, and abuse handling; structured logging; metrics; error tracking; PWA install; deployment pipelines · **Project step:** a public URL where two strangers can play; dashboards; a finished README, GIF, and demo video; `v1.0.0` · **Course:** [JavaScript — Build a Multiplayer Game](README.md) · **Previous:** [Lab 07](lab-07-engine-performance-testing.md)

---

## This lab's feature

Everything so far ran on `localhost`. The last step of any real project — and the step most student projects never take — is making it run *somewhere else*, for *someone else*, *reliably*. It is also where JavaScript's runtime story completes: Node in production is a different animal from Node on your laptop, and a WebSocket server is the most demanding thing you can deploy on a free tier.

This lab is the operational half of the language: how a Node process should behave under a process manager and a load balancer; why a WebSocket server can't be scaled the way a stateless HTTP API can; how to containerize a three-package TypeScript workspace into a small image; how to know, at 3 a.m., whether the game is up and why it isn't. By the end there's a URL in your README, a friend in another city joins your room, and a recruiter can click and play.

---

## Theory

### 1. Production Node

A Node process in production is *managed*: a supervisor (Docker, systemd, a platform's runtime) starts it, checks it, and stops it. Your job is to be a good citizen:

- **Listen on `process.env.PORT` and `0.0.0.0`** — the platform decides the port; `localhost` binding is invisible from outside the container.
- **`NODE_ENV=production`** — libraries use it to disable dev-only behavior; your code should not branch on it for anything important (config from env, per Lab 4).
- **Graceful shutdown** on `SIGTERM`: stop accepting connections (`server.close()`), tell WebSocket clients to reconnect (send a `shutdown` message, close with code `1001`), finish in-flight work, flush logs, exit `0` — all within the supervisor's grace period (~10–30 s). Deploys and autoscaling send `SIGTERM` constantly; a server that ignores it drops every player mid-match.
- **Health endpoints**: `/health` (liveness — the process responds) and `/ready` (readiness — it can serve: index loaded, no shutdown in progress). Platforms poll these to route traffic and restart you.
- **Crash on unknowns**: an `uncaughtException` or `unhandledRejection` means state you don't understand — log it and exit non-zero; let the supervisor restart a clean process. Never `process.on("uncaughtException", () => {})` to "stay up."
- **Never `--watch`, never `tsx`, never dev dependencies in production** — run compiled JavaScript (or Node's native type stripping) from a minimal install.

### 2. WebSockets in production: proxies, stickiness, and state

Between the browser and your process sit a **TLS terminator** and a **reverse proxy** (the platform's edge, or nginx/Caddy if you self-host). The browser speaks `wss://` (TLS — required; browsers refuse insecure WebSockets from `https://` pages and platforms provide certificates); the proxy must **support the `Upgrade` handshake** and must not impose short **idle timeouts** — most proxies cut a silent connection after 60 s, which is exactly why Lab 4's heartbeats exist. Check the proxy's WebSocket documentation before choosing a host.

The harder constraint: a WebSocket server is **stateful** — a room lives in *one* process's memory. Two instances behind a round-robin load balancer would split a room's players across processes that don't know about each other. Options, in order of complexity: **one instance** (correct for this course — document the limit; your Lab 7 capacity number says how many players that supports), **sticky sessions** (route by room id to a fixed instance), or **externalized state** (Redis pub/sub between instances). Know all three; do the first; explain the others in the README.

**Origin checks**: browsers send an `Origin` header on the WebSocket handshake; reject connections whose origin isn't your site (`verifyClient` in `ws`) — the WebSocket equivalent of CORS, which otherwise doesn't apply. Rate limits, payload caps, join timeouts, and slow-client policy from Lab 4 are now *the* thing standing between you and someone's script opening 10,000 connections. Cap connections per IP. Read the WebSocket section of OWASP's [HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html).

### 3. Docker for a Node workspace

A **multi-stage Dockerfile**: stage 1 (`node:22-alpine` or `-slim`) copies the whole workspace, runs `npm ci`, builds the client with Vite and compiles the server with `tsc` (or keeps `.ts` for native stripping); stage 2 starts from a clean base, copies only `server/dist`, `client/dist`, `shared/dist`, and a **production-only** install (`npm ci --omit=dev` with the workspace flags), sets `NODE_ENV=production`, runs as a **non-root user**, uses `CMD ["node", "server/dist/index.js"]` (exec form — so `SIGTERM` reaches Node, not a shell), and declares a `HEALTHCHECK`. Layer order matters for cache: copy `package*.json` first, install, *then* copy source. `.dockerignore` excludes `node_modules`, `.git`, logs. Target: **an image under 200 MB** — measure it. The Node team's [Docker best practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md) and Snyk's [10 best practices](https://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker/) cover the rest (init process, signals, `npm start` vs `node` directly).

### 4. Configuration, secrets, and the twelve factors

Everything that differs between laptop and production is an **environment variable**: `PORT`, `LOG_LEVEL`, `ALLOWED_ORIGINS`, `MAX_ROOMS`, `SENTRY_DSN`. Your zod-validated `ServerConfig` from Lab 6 fails fast on a missing or malformed value at startup — the right time to fail. **Secrets** (API keys, DSNs) live in the platform's secret store, never in the image, never in git (`.env` is in `.gitignore`; `.env.example` documents the keys). The [Twelve-Factor App](https://12factor.net/) is twenty years old and still the checklist.

### 5. Observability: logs, metrics, errors

You can't fix what you can't see. Three signals:

- **Structured logs**: JSON lines with a level, timestamp, and fields — `pino` is the fast Node standard (it moves formatting off the main thread — a Lab 4 lesson applied). Log *events* (`room.created`, `player.joined`, `ws.rejected {reason}`), not prose; include a `roomId` and `playerId` so you can filter a match. Never log secrets or full messages. Platforms collect `stdout`; that's where logs go — not files.
- **Metrics**: counters and gauges you can graph — connected players, rooms, messages/s in and out, bytes/s, tick duration p99, event-loop utilization, RSS, rejected connections by reason. Expose them on `/metrics` (Prometheus text format, via `prom-client`) or on a simple JSON stats page your own dashboard reads. The Lab 7 load-test numbers become live gauges.
- **Error tracking**: an unhandled exception in production should reach you with a stack trace. Sentry has a free tier and a Node SDK; wiring it takes twenty minutes and is optional but recommended.

Plus **uptime monitoring**: a free external checker hitting `/health` every minute and emailing you when it fails.

### 6. Deployment pipelines

Continuous delivery means a **git tag deploys**. Extend Lab 7's GitHub Actions: on tag `v*`, build the image, push it to a registry (GitHub Container Registry is free), and trigger the platform's deploy (`flyctl deploy`, Render's deploy hook, Railway's CLI) — with the platform's token as a repository secret. **Platform choice** for a WebSocket server on a free/cheap tier: [Fly.io](https://fly.io/docs/js/) (containers, WebSockets fine, regions incl. Europe), [Render](https://render.com/docs/deploy-node-express-app) (simple; free tier spins down on idle — the first player waits ~30 s, which you should mention in the README or avoid), Railway, or a €4 VPS with Caddy for automatic TLS. **Client hosting**: serve `client/dist` from the Node server (simplest — one origin, no CORS) or push it to Cloudflare Pages / GitHub Pages and point the WebSocket at the server URL. A version stamp (git SHA) in the HUD and in `/health` lets you confirm what's running.

### 7. Finish like a professional

- **PWA**: a `manifest.json`, icons, and a minimal service worker (Vite's PWA plugin) make the game installable on phones and desktops — a five-minute win that impresses.
- **itch.io** accepts HTML5 uploads: publish the client there (pointing at your server) for a games audience alongside the GitHub audience.
- **The README** is now the product page: hero GIF (two players), live URL, "how to play," architecture diagram (client / shared / server, the protocol, the loop), the measurement tables from Labs 5 and 7, the capacity number and its bottleneck, known limitations (one instance; interpolation delay; no lag compensation — or whatever is true), how to run locally in three commands, and the semester's tag history.
- **Demo video**: 3–5 minutes — gameplay with two windows, netgraph on, then a tour of the architecture and one deep dive (prediction or GC). Recruiters watch videos; they rarely clone repos.

### Prove it to yourself (terminal, 15 minutes)

1. Run your server; `kill -TERM <pid>`. Does it exit within 5 s with code 0 and do connected clients get a close frame? Now with `CMD npm start` in a container vs `CMD ["node", …]` — `docker stop` and time it (the default grace is 10 s, then `SIGKILL`).
2. `docker build` twice with a one-line source change; compare build times with `package*.json` copied before vs. after the source. Check the image size with `docker images`.
3. Point the client at `ws://` from an `https://` page — read the browser's error. That's why WSS is mandatory.
4. Open a WebSocket to your server from a page on a different origin (`new WebSocket("wss://your.app/ws")` in the console of any site). With no origin check it connects. Add `verifyClient`; retry.
5. `curl -s localhost:3000/metrics` while a bot match runs. Then `kill -STOP` the process for 3 s and `kill -CONT` — what did `/health` do and what did the event-loop-utilization gauge show?

---

## Project step: a URL, two strangers, and a finished product

### Milestones

**M1 — Production-ready process.**
Graceful `SIGTERM` (server close → `shutdown` message + close code `1001` → flush → exit 0, under 10 s); `/health` and `/ready`; crash-on-unknown with logged stack; `pino` structured logging with `roomId`/`playerId` fields and a `LOG_LEVEL` env; `prom-client` `/metrics` (or a JSON stats page) with players, rooms, msg/s, bytes/s, tick p99, event-loop utilization, RSS, rejections by reason; a version stamp (git SHA at build) in `/health` and the HUD. Zod-validated config with `ALLOWED_ORIGINS`, `MAX_CONNECTIONS_PER_IP`, `MAX_ROOMS`, `MAX_PLAYERS_PER_ROOM`.

**M2 — Hardening.**
Origin verification on the handshake; per-IP connection cap; the Lab 4 limits (payload, rate, join timeout, slow-client) confirmed under load with Lab 7's load-test script pointed at a **staging** container; a **chaos test**: kill a client mid-match, kill the *server* mid-match (players should reconnect with backoff and land in the lobby with a clear message), and a client sending garbage frames at 1,000/s (should be closed, logged, counted in metrics, and not affect other rooms' tick time — prove that last part with the metric).

**M3 — Container and pipeline.**
Multi-stage `Dockerfile` for the workspace; non-root; exec-form `CMD`; `HEALTHCHECK`; `.dockerignore`; image < 200 MB (record the size). `docker compose` for local production-like runs. GitHub Actions: on `v*` tags → build → push to GHCR → deploy to your platform; the existing CI still gates every push. Deploy. **WSS works** from the public URL; heartbeats keep connections alive through the proxy; the `/health` version matches the tag.

**M4 — Launch and finish.**
Get **two people you don't share a network with** to play a match at the same time; record it (GIF/video) and put their (anonymized) netgraph numbers in the README — real-world RTT is the most honest measurement in the whole course. Uptime monitor on `/health`. PWA manifest + install tested on a phone. Optional itch.io page. The README rewritten as a product page (Section 7); the architecture diagram; the consolidated measurement tables (JSON vs binary, before/after GC, capacity chart); known limitations with the *reason* for each; a **"What I'd do next"** section (sticky sessions or Redis for multi-instance, lag compensation, matchmaking, accounts). Demo video linked. Tag `v1.0.0`. Prepare the **5-minute showcase**: play (with a classmate) for 60 s, then one deep dive of your choice.

### Definition of done

- Graceful shutdown, `/health` + `/ready`, structured logs, `/metrics`, version stamp, validated config.
- Origin check, per-IP cap, all limits verified under load; chaos tests documented with metrics proving isolation.
- Multi-stage image < 200 MB, non-root, exec-form `CMD`, `HEALTHCHECK`; tag-triggered deploy pipeline; public WSS URL live.
- Two remote strangers played; their RTT and your metrics dashboard in the README; uptime monitor active.
- PWA installable; README as product page with GIF, architecture, all measurements, limitations, next steps; demo video; `v1.0.0`.
- Repo tagged `lab-08` and `v1.0.0`.

---

## Deliverable checklist

- [ ] `SIGTERM` → `server.close()` → `shutdown` message + `1001` → flush → exit 0 in < 10 s; tested with `docker stop`.
- [ ] `/health` (liveness), `/ready` (readiness), version stamp; crash-on-unknown with logged stack.
- [ ] `pino` JSON logs with `roomId`/`playerId`; `LOG_LEVEL` env; no secrets logged.
- [ ] `/metrics`: players, rooms, msg/s, bytes/s, tick p99, event-loop utilization, RSS, rejections by reason.
- [ ] Zod config: `ALLOWED_ORIGINS`, per-IP cap, room/player caps; `.env.example`; secrets in platform store.
- [ ] Origin verification; per-IP connection cap; chaos tests (client kill, server kill + reconnect, garbage flood) documented with isolation metric.
- [ ] Multi-stage Dockerfile, non-root, exec `CMD`, `HEALTHCHECK`, `.dockerignore`; image size recorded (< 200 MB); `docker compose` local run.
- [ ] GitHub Actions: CI on push; tag `v*` → build → GHCR → deploy; live public WSS URL; heartbeats survive proxy idle timeout.
- [ ] Two remote strangers' match recorded; their RTT in README; uptime monitor on `/health`.
- [ ] PWA manifest + install tested; optional itch.io page.
- [ ] README as product page (GIF, URL, how to play, architecture diagram, all measurement tables, capacity + bottleneck, limitations with reasons, run-locally-in-3-commands, tag history, "What I'd do next"); demo video.
- [ ] Git tags `lab-08` and `v1.0.0`; 5-minute showcase ready.

---

## Reflection — explain it at the whiteboard

1. Walk through what your process does between receiving `SIGTERM` and exiting. Why does `CMD npm start` break this? Why does ignoring `SIGTERM` drop players?
2. Why is a WebSocket server harder to scale horizontally than a REST API? Describe sticky sessions and the Redis pub/sub design. Which did you ship and why?
3. Why must the client use `wss://`? Where is TLS terminated in your deployment, and what does that mean for the proxy's WebSocket support and idle timeouts?
4. CORS doesn't apply to WebSockets — so what stops another site's page from connecting to your server as its visitors? Where do you check it?
5. Liveness vs readiness — what does each answer, and what does the platform do differently with each?
6. Why structured JSON logs to stdout rather than formatted text to a file? Why does `pino` move formatting off the main thread — which lab's lesson is that?
7. Multi-stage Docker build: what's in stage 1 that must not be in stage 2, and why? Why copy `package*.json` before the source?
8. Your load test said capacity N. A stranger's RTT was X ms. Put those two numbers together: how many concurrent players in Europe can your one instance serve well, and what would you change first?
9. If the server crashes at 3 a.m., how do you find out, and what do you look at first?

---

## Stretch

Run **two server instances** behind a proxy with **sticky routing by room id** (Caddy or nginx `hash` upstream; or Fly's regions), and prove players in the same room land on the same instance while different rooms spread across both; then replace stickiness with **Redis pub/sub** relaying room events so a room can span instances, and measure the added latency. Add **Sentry** (or equivalent) error tracking and trigger a deliberate exception from a bot to see the full stack in the dashboard. Finally, produce a **one-page postmortem** of the worst production issue you hit during the lab — timeline, root cause, fix, prevention — in the format real engineering teams use; recruiters love this document more than any feature.

---

## Resources

**Watch**

- Fireship — [Learn Docker in 7 Easy Steps (12 min)](https://www.youtube.com/watch?v=gAkwW2tuIqE). Dockerfile, layers, multi-stage, compose — fast and accurate; enough to start M3.
- Hussein Nasser — [WebSockets Crash Course](https://www.youtube.com/watch?v=2Nt-ZrNP22A) — rewatch the "scaling and proxies" portion now that it's your problem.

**Read**

- Node.js Docker team — [Docker and Node.js Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md) — signals, `CMD` exec form, non-root, memory, and the `node` vs `npm start` question. Short and authoritative.
- Snyk — [10 best practices to containerize Node.js web applications with Docker](https://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker/). Multi-stage builds, `.dockerignore`, deterministic installs, `dumb-init`, scanning. The checklist for M3.
- Node.js API — [`process` signal events](https://nodejs.org/api/process.html#signal-events) for graceful shutdown; [`ws` README](https://github.com/websockets/ws) for `verifyClient`, `maxPayload`, and heartbeats.
- OWASP — [HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html) — the "Web Sockets" section: origin, TLS, input validation, rate limiting.
- [The Twelve-Factor App](https://12factor.net/) — config, logs as streams, disposability (graceful shutdown). Read all twelve; they're short.
- [pino](https://getpino.io) — structured logging; why it's fast. [`prom-client`](https://github.com/siimon/prom-client) for `/metrics`.
- [Fly.io — JavaScript on Fly](https://fly.io/docs/js/) and [Render — Deploy a Node app](https://render.com/docs/deploy-node-express-app). Pick one; check the WebSocket notes.
- MDN — [Progressive web apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps) (manifest, installability). [itch.io — HTML5 games](https://itch.io/docs/creators/html5) for the optional games-audience release.
- GitHub — [Building and testing Node.js](https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-nodejs) — extend for the tag-triggered deploy job.
