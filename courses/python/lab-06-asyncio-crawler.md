# Lab 06 — The Async Crawler: `asyncio`, Coroutines, and Structured Concurrency

> "Async is not about speed. It's about waiting well."

**Weeks:** 11–12 · **Language focus:** the event loop, coroutines and `await`, tasks, `TaskGroup`, cancellation and timeouts, semaphores and queues, async iterators, `httpx` · **Project step:** a polite, fast, async web crawler that feeds new documents into the corpus · **Course:** [Python — Build a Search Engine](README.md) · **Previous:** [Lab 05](lab-05-concurrency-and-the-gil.md)

---

## This lab's feature

Lab 5 ended with a question: what about work that is neither CPU-bound nor a good fit for threads — thousands of network requests, most of the time spent *waiting*? A thread per request is heavy; a pool of 20 threads means at most 20 requests in flight. **`asyncio`** lets one thread juggle thousands of in-flight requests by switching between them *exactly when each one starts waiting*. It's the model behind every modern Python web framework (FastAPI, Lab 7), every async database driver, and most of the network-heavy Python written today.

The beautiful part: you already know the mechanism. A coroutine is a generator that yields to a scheduler instead of to a `for` loop. Lab 1's `yield` was the first half of this story; Beazley's "concurrency from the ground up" talk builds an event loop from generators live on stage. This lab makes that concrete by building the thing search engines are named after — a **crawler** — that fetches pages concurrently, politely, and without ever blocking the loop.

---

## Theory

### 1. Cooperative concurrency and the event loop

Threads are **preemptive**: the OS interrupts them whenever it likes. Coroutines are **cooperative**: a coroutine runs until it *voluntarily* gives up control at an `await`, and only then can another run. A single **event loop** in a single thread does the scheduling: it keeps a queue of ready tasks, runs one until it awaits something not yet ready (a socket read, a timer), registers interest in that event with the OS (`select`/`epoll`/`kqueue`), and picks the next ready task.

Consequences:

- **No data races on shared state between awaits.** Between two `await`s, your code runs uninterrupted. You rarely need locks. (You need them again the moment you `await` in the middle of a multi-step update.)
- **One blocking call freezes everything.** `time.sleep(1)`, `requests.get(...)`, a big `json.loads`, a CPU-heavy loop — none of them `await`, so the loop can't switch. Every other task stalls. This is *the* asyncio bug; Section 6 covers the fixes.
- **Throughput comes from overlap, not parallelism.** One thread, one core. 1,000 requests in flight means 1,000 waits overlapping — not 1,000 things computing.

### 2. Coroutines, `await`, and tasks

```python
async def fetch(client: httpx.AsyncClient, url: str) -> str:
    resp = await client.get(url)          # suspends here until the response arrives
    return resp.text
```

`async def` defines a **coroutine function**. Calling it runs nothing — it returns a **coroutine object** (exactly like calling a generator function returned a generator in Lab 1). `await coro` runs it to completion, suspending the *current* coroutine whenever the awaited one suspends. `asyncio.run(main())` creates the loop, runs `main` to completion, and tears the loop down.

A bare coroutine runs *sequentially* when awaited. To run things *concurrently*, wrap them in **tasks** — the loop schedules tasks independently:

```python
async with asyncio.TaskGroup() as tg:                  # Python 3.11+
    results = [tg.create_task(fetch(client, u)) for u in urls]
# all tasks are done here; if any raised, the group cancelled the rest and re-raises
pages = [t.result() for t in results]
```

`asyncio.gather(*coros)` is the older equivalent; `TaskGroup` is what you should use, because of the next section. The one thing to remember about `create_task` outside a group: **keep a reference** to the task, or it can be garbage-collected mid-flight and silently vanish.

### 3. Structured concurrency: tasks have a lifetime and a parent

Nathaniel Smith's essay ["Notes on structured concurrency, or: Go statement considered harmful"](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/) argues that fire-and-forget task spawning is `goto` for concurrency: you can't reason about what's running, errors get lost, cleanup is impossible. The alternative — **structured concurrency** — says every task lives inside a *scope* that waits for it, and an error in one cancels its siblings and propagates to the parent.

`asyncio.TaskGroup` (3.11) is that scope. When the `async with` block exits, every task started in it has finished. If one raises, the others are **cancelled** and the exception (wrapped in an `ExceptionGroup`) surfaces where you can `except*` it. Your crawler's fetch fan-out belongs in a `TaskGroup`; so does anything else where "start N things, wait for all, fail together" is the shape.

**Cancellation** is how asyncio stops a task: it throws `CancelledError` at the task's current `await`. Your code should let it propagate (don't `except Exception` around awaits without re-raising `CancelledError` — it's a `BaseException` for exactly this reason) and use `try/finally` for cleanup. **Timeouts** are cancellation with a clock: `async with asyncio.timeout(10):` cancels whatever is inside if it takes too long. Every network call in your crawler gets one.

### 4. Bounding concurrency: semaphores, queues, and politeness

Unbounded concurrency is a denial-of-service attack on whoever you're crawling (and on your own file descriptors). Two tools:

- **`asyncio.Semaphore(n)`** — at most `n` coroutines inside the `async with sem:` block at once. A global semaphore bounds total in-flight requests; a **per-host** semaphore (a `dict[str, Semaphore]`) bounds requests to any one server — the polite thing, and what real crawlers do.
- **`asyncio.Queue`** — the producer/consumer channel. A crawler is exactly this: a **frontier** queue of URLs to visit; N worker coroutines pull a URL, fetch it, parse links, push new URLs. `queue.join()` waits until every item has been `task_done()`. This is the shape of most real async programs.

Politeness also means: read and obey [`robots.txt`](https://developers.google.com/search/docs/crawling-indexing/robots/intro) via `urllib.robotparser`; send an honest `User-Agent` with a contact URL; **rate-limit per host** (a minimum delay between requests to the same server; `asyncio.sleep` is your friend — it's the one sleep that doesn't block); stay within the domains you were asked to crawl; and stop at `--max-pages`.

### 5. Retries, backoff, and failure

Networks fail. Your crawler must expect 429 (too many requests), 5xx, timeouts, connection resets, and malformed HTML — and *keep going*. The pattern: retry transient failures with **exponential backoff plus jitter** (`delay = min(cap, base * 2**attempt) + random.uniform(0, 1)`), give up after N attempts, log and continue. Never retry a 404. Honor `Retry-After` on a 429. Record per-URL status so a run is *reproducible*: a crawl log of (url, status, bytes, elapsed).

### 6. Don't block the loop

Four ways code blocks the loop, and the fix for each:

1. **Blocking I/O libraries** (`requests`, `open().read()` on large files, `sqlite3`). Use async-native ones (`httpx.AsyncClient`, `aiofiles`, `aiosqlite`) — or wrap the call in **`await asyncio.to_thread(fn, *args)`**, which runs it in a thread pool and awaits the result. This is Lab 5's threads, correctly used: for I/O only.
2. **CPU-heavy work** (tokenizing and indexing the fetched page). Either do it *after* the crawl (crawl writes raw documents; `findex index` runs separately), or hand it to a `ProcessPoolExecutor` via `loop.run_in_executor(pool, fn, arg)`. Never do a second of CPU work inside a coroutine.
3. **`time.sleep`**. It's `asyncio.sleep`. Always.
4. **Forgotten `await`.** `client.get(url)` without `await` returns a coroutine object that never runs, and Python warns `coroutine ... was never awaited`. Turn on `PYTHONASYNCIODEBUG=1` (or `asyncio.run(main(), debug=True)`) during development — it also flags callbacks that block the loop for >100 ms.

### 7. Async iteration and async context managers

`async for item in agen:` iterates an **async generator** — `async def` with `yield` — which can `await` between items. Your crawler's natural interface is `async def crawl(seeds) -> AsyncIterator[Page]:` — a stream of pages the consumer can write, index, or count as they arrive, exactly as Lab 1 streamed documents. `async with` is the context manager protocol with `__aenter__`/`__aexit__`; `httpx.AsyncClient` is one (it owns a connection pool; open it once per crawl, not per request — connection reuse is a large part of async's speed).

`asyncio` also has `as_completed`, `wait`, `Event`, `Lock`, `Condition`, and `run_in_executor`; the [task docs](https://docs.python.org/3/library/asyncio-task.html) and [synchronization docs](https://docs.python.org/3/library/asyncio-sync.html) are short and worth reading once end-to-end.

### Prove it to yourself (REPL/terminal, 15 minutes)

1. `async def f(): return 1` — call `f()`. What do you get? Now `asyncio.run(f())`. Relate this to calling a generator function in Lab 1.
2. Three coroutines that each `await asyncio.sleep(1)`. Await them sequentially (3 s). Then in a `TaskGroup` (1 s). Then replace `asyncio.sleep` with `time.sleep` in the group version — 3 s again. Why?
3. A `TaskGroup` with one task that raises after 0.1 s and another that sleeps 10 s. How long does the block take? What is the exception type? Catch it with `except*`.
4. Fetch 30 URLs with `httpx.AsyncClient`, first with a new client per request, then one shared client. Time both. Connection reuse is the difference.
5. `asyncio.run(main(), debug=True)` with a `time.sleep(0.5)` inside a coroutine. Read the warning it prints.

---

## Project step: `findex crawl`

**Ethics first.** Crawl only sites you're allowed to: your own, documentation sites whose `robots.txt` permits it, your university's public pages *with permission*, or a local mirror you set up. Obey `robots.txt`, identify yourself, rate-limit, and stop at your page budget. A crawler that ignores these is abuse, not engineering — and it's the first thing an experienced reviewer checks.

### Milestones

**M1 — A single polite fetch.**
`crawler/fetch.py` — `async def fetch(client, url, *, timeout=10.0) -> FetchResult` with `asyncio.timeout`, a status/bytes/elapsed record, retries with exponential backoff + jitter for 429/5xx/timeouts (max 3), `Retry-After` honored, no retry on 4xx other than 429. `robots.py` — `RobotsCache` that fetches and caches `robots.txt` per host and answers `allowed(url)`. Honest `User-Agent` string with a contact URL. Tests with `httpx.MockTransport` (no network in tests).

**M2 — The frontier and the workers.**
`crawler/crawl.py` — `async def crawl(seeds, *, max_pages, concurrency, per_host, allowed_domains) -> AsyncIterator[Page]`: an `asyncio.Queue` frontier; `concurrency` worker tasks in a `TaskGroup`; a global semaphore plus per-host semaphores and per-host minimum delay; URL **canonicalization** (scheme/host lowercase, fragment stripped, trailing slash normalized, query sorted) and a `seen` set so nothing is fetched twice; link extraction with [`selectolax`](https://selectolax.readthedocs.io/) (fast) or `html.parser`; text extraction into `Page(url, title, text, fetched_at)`. Stop cleanly at `max_pages` — cancel workers, drain, close the client.

**M3 — Wire it into `findex`.**
`findex crawl <seed-url> [--max-pages 500] [--concurrency 10] [--per-host 2] [--out data/crawl.jsonl]` — writes one JSON line per page (streaming, as pages arrive — never buffer them all) so `iter_documents` from Lab 1 can read it and `findex index` can index it. A `rich` live display: pages fetched, pages/s, in-flight, errors, queue depth. A `crawl.log` with per-URL status. All indexing stays *outside* the event loop.

**M4 — Benchmark and explain.**
Same seed, same `max_pages` (≥ 200), `concurrency ∈ {1, 5, 20}`:

| Concurrency | Pages | Wall (s) | Pages/s | Errors | Peak RSS |
|---|---|---|---|---|---|
| 1 (effectively sequential) | | | | | |
| 5 | | | | | |
| 20 | | | | | |

Then the README section: why concurrency 20 in one thread beat Lab 5's approach for this workload, what the per-host limits cost you (and why you kept them), where the loop would have blocked if you'd indexed inline, and one failure you handled (a 429, a timeout, a redirect loop) with the log lines to prove it.

### Definition of done

- `fetch` has timeouts, retries with backoff + jitter, and `Retry-After` handling; tested via `MockTransport`.
- `robots.txt` obeyed; honest `User-Agent`; per-host concurrency and delay limits; domain allowlist; `max_pages` respected.
- `crawl` is an async generator over a `Queue`-based frontier with `TaskGroup` workers; no duplicate fetches; clean shutdown.
- Output streams to JSON lines that `findex index` consumes; live progress display; per-URL log.
- No blocking calls in coroutines (verified with `debug=True`); CPU work stays outside the loop.
- Benchmark table for 3 concurrency levels and the explanation in the README.
- Repo tagged `lab-06`.

---

## Deliverable checklist

- [ ] `fetch` with `asyncio.timeout`, bounded retries with exponential backoff + jitter, `Retry-After`, status logging; `MockTransport` tests.
- [ ] `RobotsCache`; honest `User-Agent`; per-host semaphore + minimum delay; global concurrency semaphore; domain allowlist.
- [ ] `Queue` frontier + `TaskGroup` workers; URL canonicalization + `seen` set; async generator interface; clean stop at `max_pages`.
- [ ] `findex crawl` streaming JSON-lines output consumed by `findex index`; `rich` live stats; `crawl.log`.
- [ ] No blocking calls in coroutines (`debug=True` clean); indexing outside the loop.
- [ ] Benchmark table at concurrency 1/5/20 and the explanation section; one handled failure shown with logs.
- [ ] Ethics: permission for the crawled site stated in the README.
- [ ] Git tag `lab-06`.

---

## Reflection — explain it at the whiteboard

1. Draw the event loop. What happens at an `await` on a socket read? How does the loop know when to resume that task?
2. Cooperative vs preemptive concurrency — one advantage and one danger of each. Why do you rarely need locks in asyncio, and when do you suddenly need them again?
3. `time.sleep(1)` in a coroutine — what happens to the other 19 workers? What's the fix, and why does `asyncio.sleep` behave differently?
4. Relate `async def`/`await` to generators and `yield`. What's a coroutine object, and why does calling `fetch(url)` do nothing?
5. Why `TaskGroup` over `gather`? What happens to sibling tasks when one raises? What is an `ExceptionGroup`?
6. Your crawler is fast at concurrency 20 in one thread; Lab 5's threaded indexer was not. Reconcile those two facts.
7. Why is `CancelledError` a `BaseException`? What breaks if you `except Exception:` around an `await`?
8. How does a per-host semaphore differ from a global one, and why do you need both? What does `Retry-After` change about your backoff?
9. Where would CPU work go if you *had* to do it during the crawl?

---

## Stretch

Make the crawler **resumable**: persist the frontier and `seen` set to disk (SQLite via `aiosqlite`) so `Ctrl-C` and re-run continues where it stopped. Then add **incremental indexing**: pages already indexed are skipped unless their `ETag`/`Last-Modified` changed (conditional requests with `If-None-Match`). Finally, compare `asyncio` against `trio` (the library structured concurrency came from) or `anyio` by porting `crawl()` — notice what's the same, and what `trio` makes impossible to get wrong.

---

## Resources

**Watch**

- Łukasz Langa — [*import asyncio: Learn Python's AsyncIO* (YouTube series, ~6 × 30–60 min)](https://www.youtube.com/playlist?list=PLhNSoGM2ik6SIkVGXWBwerucXjgP1rHmB). The CPython release manager teaching asyncio from the event loop up — including building a loop by hand. The most careful asyncio material anywhere. Episodes 1–4 are this lab.
- David Beazley — [Python Concurrency From the Ground Up: LIVE! (PyCon 2015)](https://www.youtube.com/watch?v=MCs5OvhV9S4). You watched it in Lab 5; watch it again now that you've written `await`. The moment he swaps `yield` for the event loop is the moment asyncio stops being magic.
- Miguel Grinberg — [Asynchronous Python for the Complete Beginner (PyCon 2017, 30 min)](https://www.youtube.com/watch?v=iG6fr81xHKA). The gentlest correct explanation of what async buys you and when it doesn't. Watch first if Section 1 felt abstract.
- David Beazley — [Generators: The Final Frontier (PyCon 2014, 3h50)](https://www.youtube.com/watch?v=D1twn9kLmYg). The deep end: how coroutines were built out of generators, `yield from`, and the design space asyncio came from. Optional; for the curious.

**Read**

- Real Python — [Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/). Long, correct, with a chain-of-requests example close to a crawler. The single best written intro.
- Python docs — [`asyncio` — Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html) (read all of it: `TaskGroup`, timeouts, cancellation, `to_thread`) and [Synchronization Primitives](https://docs.python.org/3/library/asyncio-sync.html).
- Nathaniel J. Smith — [Notes on structured concurrency, or: Go statement considered harmful](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/). The essay that led to `TaskGroup`. Long, foundational, worth every minute.
- [httpx — Async Support](https://www.python-httpx.org/async/). The client you'll use; read about connection pooling, timeouts, and `MockTransport` for tests.
- Google Search Central — [Introduction to robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro) and Python's [`urllib.robotparser`](https://docs.python.org/3/library/urllib.robotparser.html).
- *Fluent Python*, 2nd ed. — Chapter 21 ("Asynchronous Programming"). Includes an async crawler-flavored example.
