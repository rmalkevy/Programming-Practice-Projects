# Lab 07 — Search on the Web: FastAPI, Pydantic, ASGI, and Deployment

> "A search engine nobody can reach is a data structure."

**Weeks:** 13–14 · **Language focus:** ASGI and the request lifecycle, FastAPI, Pydantic models and validation, dependency injection, app lifespan, sync vs async endpoints, settings from the environment, Docker, deployment · **Project step:** a search API and web UI, live at a public URL, load-tested · **Course:** [Python — Build a Search Engine](README.md) · **Previous:** [Lab 06](lab-06-asyncio-crawler.md)

---

## This lab's feature

Everything you've built runs in your terminal. This lab puts it on the internet: an HTTP API that any client can call, a small web page anyone can search from, a public URL you can put on your CV.

The tool is **FastAPI** — the Python web framework that grew out of exactly the ideas you've spent six labs on. Its routing is `asyncio` (Lab 6). Its request validation is **type hints** (Lab 4) read at import time by **Pydantic**. Its dependency injection is functions and closures (Lab 3). Its startup logic is a context manager (Lab 3). You will recognize every piece, which is why this lab is less about learning a framework and more about seeing how the language features compose into one. And you'll learn the parts of shipping a service that no framework does for you: configuration, containers, health checks, and load testing.

---

## Theory

### 1. HTTP in one paragraph, ASGI in another

An HTTP request is a method (`GET`, `POST`…), a path (`/search`), headers, and optionally a body; the response is a status code (`200`, `404`, `422`…), headers, and a body — typically JSON for APIs, HTML for pages. Read [MDN's HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) once if any of that is fuzzy; the rest of the lab assumes it.

A Python web server needs a contract with the framework. The old one is **WSGI** (Flask, Django-classic): a synchronous function per request; one worker thread or process per in-flight request. The modern one is [**ASGI**](https://asgi.readthedocs.io/): an `async` callable, which lets one worker handle thousands of concurrent connections the Lab 6 way. An **ASGI server** — [Uvicorn](https://uvicorn.dev/) — owns the sockets and the event loop and calls your app for each request. FastAPI is an ASGI app (built on Starlette). `uvicorn findex.web:app` is the whole deployment story in development.

### 2. FastAPI: routes are typed functions

```python
@app.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1, max_length=200),
    k: int = Query(10, ge=1, le=100),
    scorer: Literal["bm25", "tfidf"] = "bm25",
    index: Index = Depends(get_index),
) -> SearchResponse:
    ...
```

Everything here is something you've already learned, doing a new job:

- **Path and query parameters** come from the function signature. Type hints (Lab 4) drive parsing and validation: `k: int` rejects `?k=abc` with a `422` and a JSON error body — you write no validation code.
- **`Literal`** becomes an enum in the docs and a 422 for anything else.
- **`response_model`** declares the output schema; FastAPI validates and serializes it, and generates the **OpenAPI** document — which is why `/docs` gives you an interactive API browser for free. That URL is a portfolio artifact by itself.
- **`Depends(get_index)`** is dependency injection (next section).

Watch [Sebastián Ramírez's talk](https://www.youtube.com/watch?v=mwvmfl8nN_U) on how FastAPI was designed to make type hints do all this work; it's the philosophy of your Lab 4 in someone else's framework.

### 3. Pydantic: dataclasses that validate

[Pydantic](https://docs.pydantic.dev/latest/) models look like dataclasses but **validate and coerce on construction**: `SearchResult(doc_id="12", score=0.9)` yields `doc_id == 12` (coerced) or a precise `ValidationError`. Pydantic v2's core is written in Rust and is fast. It is the boundary layer: **untrusted data in (requests, config, JSON files) → validated Python objects.** Your internal `dataclass`es from Lab 2–3 stay as they are; you add Pydantic models at the edges (`SearchRequest`, `SearchResult`, `SearchResponse`, `Settings`) and convert between them — a small, deliberate seam.

Also from Pydantic: [`pydantic-settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — a `Settings(BaseSettings)` class that reads `INDEX_PATH`, `LOG_LEVEL`, `PORT` from environment variables (and a `.env` file in development), validated and typed. That's the **12-factor** config rule ([12factor.net](https://12factor.net/), rule III): config lives in the environment, never in code, so the same container runs in dev and prod.

### 4. Dependency injection and app lifespan

`Depends(fn)` means: before calling the route, call `fn` (which may itself have dependencies, and may be `async`, and may be a generator for setup/teardown), and pass its return value in. It's how you get the index, the settings, the current user, a database session — without globals and with full testability (`app.dependency_overrides[get_index] = lambda: tiny_test_index`).

The index itself is loaded **once**, at startup, not per request. That's the **lifespan** context manager:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.index = load(settings.index_path)      # startup: Lab 3's loader
    yield
    app.state.index.close()                          # shutdown
```

It's Lab 3's `@contextmanager` pattern, async. `get_index` just returns `request.app.state.index`.

### 5. Sync vs async endpoints — and not blocking the loop, again

FastAPI lets you write `def` *or* `async def` routes. The rule from [the FastAPI docs on concurrency](https://fastapi.tiangolo.com/async/): if your handler `await`s async libraries, make it `async def`; if it calls **blocking** code (your CPU-bound BM25 scoring, a sync database driver), make it a plain **`def`** — FastAPI then runs it in a thread pool so it doesn't block the event loop. Writing `async def` around blocking code is the Lab 6 bug in a new outfit, and it's the most common FastAPI performance mistake. Your `search` endpoint does CPU work: it should probably be `def`, or `async def` with `await asyncio.to_thread(...)`. Benchmark both in M4.

**Background tasks** (`BackgroundTasks`) let a route return immediately and finish work afterward — logging the query to a file, warming a cache. For anything heavy or that must survive a restart, you'd want a real queue; know the distinction.

### 6. The web UI: templates, or htmx

You need a page with a search box and results. Two honest options for a Python developer who isn't taking a frontend course:

- **Jinja2 templates** served by FastAPI: `GET /` renders `index.html`; the form submits to `GET /?q=...` and the same template renders results. Server-rendered, zero JavaScript, entirely sufficient.
- **[htmx](https://htmx.org/)**: the same templates, plus one script tag, and the form fetches results into the page without reload (`hx-get="/search-fragment" hx-target="#results" hx-trigger="keyup changed delay:300ms"`). Search-as-you-type in ten lines of HTML.

Either way: highlight the matched terms in snippets (Lab 3 gives you positions), show the score if you like, link to a `GET /docs/{doc_id}` page that renders the full document, and make it look intentional — a system font, some whitespace, a max-width. Keep the API and the UI in the same app; the UI is just routes that return HTML.

### 7. Containers and deployment

A **Dockerfile** makes "runs on my machine" into "runs anywhere." The [uv Docker guide](https://docs.astral.sh/uv/guides/integration/docker/) is the template: a multi-stage build — install dependencies from `uv.lock` in a builder stage, copy the environment into a slim runtime image, run as a non-root user, `CMD ["uvicorn", "findex.web:app", "--host", "0.0.0.0", "--port", "8000"]`. Your index file is either baked into the image (simple; fine for a portfolio demo) or mounted/downloaded at startup (production-shaped).

Deployment targets with a free tier that accept a Dockerfile: [Render](https://render.com/docs/deploy-fastapi), [Fly.io](https://fly.io/docs/python/frameworks/fastapi/), Railway. Any of them: connect the GitHub repo, set environment variables, deploy on push. You need: a **`/health`** endpoint the platform can probe, **structured logs** to stdout (Lab 4's logging, JSON-formatted if you want to look professional), a **CORS** policy if a separate frontend ever calls the API, and **graceful shutdown** (uvicorn handles `SIGTERM`; your lifespan's teardown runs).

### 8. Load testing: what "fast" means

Nobody believes "it's fast." They believe **p50 / p95 / p99 latency at N requests per second**. Tools: [`oha`](https://github.com/hatoo/oha) or [`hey`](https://github.com/rakyll/hey) — `oha -z 30s -c 50 "http://localhost:8000/search?q=python"` runs 50 concurrent clients for 30 s and prints the distribution. Run it against your deployed URL too. Then read the numbers: p99 ≫ p50 usually means the GIL (Lab 5) or a blocking call (Lab 6) or GC pauses; compare `def` vs `async def` for your search route and multiple uvicorn workers (`--workers 4`, one process per core — Lab 5 again) and you have a real performance story for the README.

### Prove it to yourself (terminal, 15 minutes)

1. A one-route FastAPI app. `curl "localhost:8000/search?k=abc"`. Read the 422 body. Now open `/docs`. Who wrote that page?
2. `SearchResult(doc_id="12", score="0.9")` with a Pydantic model — what are the types of the fields after construction? Now `doc_id="twelve"`.
3. Put `time.sleep(2)` in an `async def` route; hit it from two terminals at once. Total time? Change to `def`. Again.
4. Set `INDEX_PATH` in the environment and read it via `pydantic-settings`. Then set it to a path that doesn't exist — where does the error surface, and how early?
5. `oha -z 10s -c 20` against your search route. Read p50 and p99. Add `--workers 4` to uvicorn. Again.

---

## Project step: `findex serve`, live

### Milestones

**M1 — The API.**
`src/findex/web/` — a FastAPI app with a `lifespan` that loads the index once from `Settings.index_path`; `get_index` / `get_settings` dependencies; routes:

- `GET /search?q=&k=&scorer=&page=` → `SearchResponse{query, total, took_ms, results: [SearchResult{doc_id, title, score, snippet}]}` with validation on every parameter and **pagination**.
- `GET /docs/{doc_id}` → the document (404 via `HTTPException` if unknown).
- `GET /stats` → index size, doc count, vocabulary, uptime.
- `GET /health` → `{"status": "ok"}` and a 503 if the index isn't loaded.

Pydantic models at the edges; your Lab 2–3 dataclasses inside. Errors are JSON with a `detail` field; unexpected exceptions are logged with a request id and returned as a clean 500. `findex serve [--port 8000] [--workers 1]` wraps uvicorn so the CLI stays the entry point.

**M2 — Tests and the sync/async decision.**
`fastapi.testclient.TestClient` (or `httpx.AsyncClient` with `ASGITransport`) tests for every route, including the 422 and 404 paths, using `dependency_overrides` to inject a tiny fixture index — no real index file in tests. Then decide, with evidence, whether `search` is `def` or `async def`: time 20 concurrent requests under each and record it.

**M3 — The web UI.**
`GET /` renders a Jinja2 page: search box, results with highlighted snippets and scores, pagination links, a document view at `GET /doc/{doc_id}`. Optionally htmx for search-as-you-type. Static CSS served by FastAPI's `StaticFiles`. Should look like something you'd show a stranger — because you will.

**M4 — Ship it and measure it.**
Multi-stage `Dockerfile` (uv-based, non-root, slim); `docker run -e INDEX_PATH=... -p 8000:8000 findex` works locally. Deploy to Render / Fly.io / Railway with environment-based config; `/health` wired as the platform's health check; logs visible in the platform dashboard. **Public URL at the top of the README.** Then load-test locally *and* on the deployed instance with `oha`:

| Target | Route | Concurrency | RPS | p50 (ms) | p95 | p99 |
|---|---|---|---|---|---|---|
| local, 1 worker, `async def` | `/search` | 50 | | | | |
| local, 1 worker, `def` | `/search` | 50 | | | | |
| local, 4 workers | `/search` | 50 | | | | |
| deployed | `/search` | 20 | | | | |

Plus a paragraph connecting the numbers to Labs 5–6: which of the GIL, thread-pool offloading, and multiple processes explains each row.

### Definition of done

- Four API routes with validated parameters, pagination, proper status codes, OpenAPI docs at `/docs`.
- Index loaded once via `lifespan`; config via `pydantic-settings` from the environment; no secrets or paths in code.
- Tests via `TestClient` with `dependency_overrides`; 422/404 covered.
- Web UI with highlighted snippets, pagination, document view.
- Dockerfile builds and runs; service deployed with a working `/health`; **live URL in the README**.
- Load-test table with p50/p95/p99 and the `def` vs `async def` vs workers explanation.
- Repo tagged `lab-07`; version `0.7.0`.

---

## Resources

**Watch**

- Sebastián Ramírez — [Behind the Scenes of FastAPI and Friends for Developers and Builders (EuroPython 2025 keynote, 45 min)](https://www.youtube.com/watch?v=mwvmfl8nN_U). The creator of FastAPI, typer, and SQLModel on the design ideas behind them — type hints as the single source of truth, editor support as a feature, and how to build tools people love. The *why* behind everything in this lab.
- Sanjeev Thiyagarajan / freeCodeCamp — [Python API Development — Comprehensive Course for Beginners (19 h)](https://www.youtube.com/watch?v=0sOvCWFmrtA). You do not need all 19 hours. The first ~3 hours are the FastAPI fundamentals (path operations, Pydantic schemas, validation, docs); the deployment and Docker chapters near the end are worth it too. Use the chapter markers.

**Read**

- [FastAPI — Tutorial / User Guide](https://fastapi.tiangolo.com/tutorial/). Read in order through "Dependencies," then "Bigger Applications," "Testing," and the ["Concurrency and async / await"](https://fastapi.tiangolo.com/async/) page — the last one is Section 5 and it's the one people skip and regret.
- [Pydantic documentation](https://docs.pydantic.dev/latest/) — Models, Validators, and [Settings management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).
- [ASGI specification — Introduction](https://asgi.readthedocs.io/) and [Uvicorn docs](https://uvicorn.dev/) (deployment page: workers, `--proxy-headers`, graceful shutdown).
- MDN — [An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview). Status codes, headers, methods — the vocabulary.
- [The Twelve-Factor App](https://12factor.net/). Twelve short pages; rules III (config), VI (processes), IX (disposability), XI (logs) are this lab.
- [uv — Using uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/) — the Dockerfile template to start from — and Docker's [Python language guide](https://docs.docker.com/guides/python/).
- [htmx documentation](https://htmx.org/) — the "Introduction" and "Docs" pages; two hours to fluency.
- Deployment: [Render — Deploy a FastAPI app](https://render.com/docs/deploy-fastapi), [Fly.io — FastAPI](https://fly.io/docs/python/frameworks/fastapi/).
- Load testing: [`oha`](https://github.com/hatoo/oha) (recommended, has a live TUI) or [`hey`](https://github.com/rakyll/hey).

---

## Deliverable checklist

- [ ] `GET /search` (validated `q`, `k`, `scorer`, `page`; pagination), `GET /docs/{id}`, `GET /stats`, `GET /health`; `/docs` OpenAPI page works.
- [ ] `lifespan` loads the index once; `Depends` for index and settings; `pydantic-settings` config from env / `.env`.
- [ ] Pydantic models at the boundary; internal dataclasses unchanged; clean JSON errors; request-id logging.
- [ ] `TestClient` tests with `dependency_overrides`, covering success, 422, 404, and `/health` 503 when unloaded.
- [ ] `def` vs `async def` decision for `/search` made with timing evidence.
- [ ] Jinja2 (± htmx) UI: search, highlighted snippets, pagination, document view, static CSS.
- [ ] Multi-stage uv Dockerfile, non-root, runs locally with env config.
- [ ] Deployed; health check wired; logs visible; **public URL at the top of the README**.
- [ ] `oha` load-test table (local 1 worker × 2 modes, 4 workers, deployed) with p50/p95/p99 and explanation.
- [ ] Git tag `lab-07`.

---

## Reflection — explain it at the whiteboard

1. Trace a request from `curl` to your route function and back: what do Uvicorn, ASGI, Starlette, FastAPI, and Pydantic each do along the way?
2. WSGI vs ASGI: what changed, and why does it matter for concurrency?
3. How does FastAPI turn `k: int = Query(10, ge=1, le=100)` into a 422? Where in *your* Lab 4 knowledge does that mechanism come from?
4. Pydantic model vs `dataclass` — when do you use each in `findex`, and why not Pydantic everywhere?
5. What does `Depends` do, and how do you swap the real index for a test one without touching the route?
6. Your `search` route does 30 ms of CPU work. `def` or `async def`? What happens under 50 concurrent requests if you choose wrong?
7. Why does config come from the environment and not a `config.py`? What does the same Docker image running in dev and prod require?
8. Read your load-test table: explain the p99 difference between 1 worker and 4 workers using Lab 5.
9. What does `/health` need to check to be useful, and what happens on your platform when it returns 503?

---

## Stretch

Add **authentication** for a write path: `POST /documents` (adds a document to a pending set that a background job indexes) protected by an API key header, with **rate limiting** per key (a token bucket in memory, or Redis). Add **caching headers** (`ETag`, `Cache-Control`) to `/search` and prove with `oha` that a repeated query is served in under a millisecond. Then wire **OpenTelemetry** tracing so a single request shows up as spans (parse → score → render) in a free Grafana Cloud or Jaeger instance — and screenshot the trace for the README.
