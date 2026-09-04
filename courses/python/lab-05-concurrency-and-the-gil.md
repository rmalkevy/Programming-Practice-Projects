# Lab 05 — Concurrency and the GIL: Threads, Processes, and Why One Is 4× Faster

> "The GIL is not the problem. Your mental model of the GIL is the problem."
> — every senior Python engineer, eventually

**Weeks:** 9–10 · **Language focus:** `threading`, `multiprocessing`, `concurrent.futures`, the Global Interpreter Lock, CPU-bound vs I/O-bound, free-threaded Python 3.13 · **Project step:** parallel index construction, benchmarked and explained · **Course:** [Python — Build a Search Engine](README.md) · **Previous:** [Lab 04](lab-04-typing-testing-packaging-cli.md)

---

## This lab's feature

Your laptop has 8 or more cores. `findex index` uses one of them. This lab is about using the rest — and discovering that in Python, *how* you parallelize matters enormously, because of a single lock inside the interpreter that every Python interview asks about and most candidates explain wrong.

The **Global Interpreter Lock** means only one thread executes Python bytecode at a time. Threads still help enormously for I/O (the lock is released while waiting on a file or socket); they help *not at all* for CPU-bound Python code — and can make it slower. For CPU work you use **processes**, each with its own interpreter and its own GIL, at the cost of copying data between them. Python 3.13 added an experimental **free-threaded** build without the GIL; Python 3.14 made it officially supported. You'll benchmark all three paths on your own indexer and *see* the model instead of memorizing it.

This is one of the most valuable things you'll learn all semester, because it generalizes: I/O-bound vs CPU-bound, shared memory vs message passing, and Amdahl's law show up in every language.

---

## Theory

### 1. Concurrency vs parallelism, and the two kinds of "slow"

**Concurrency** is dealing with many things at once (structure). **Parallelism** is doing many things at once (execution, needs multiple cores). Threads in Python give you concurrency; processes (or the free-threaded build) give you parallelism.

Which one you need depends on *why* the program is slow:

- **I/O-bound** — waiting on disk, network, a database. The CPU is idle. Threads (or `asyncio`, Lab 6) let you overlap the waits. Downloading 100 pages with 20 threads is ~20× faster.
- **CPU-bound** — tokenizing, hashing, scoring. The CPU is saturated. Only more cores help — which in Python means processes, or a GIL-free build, or pushing the work into C (numpy, Lab 8).

Indexing is mostly CPU-bound (tokenization, dict updates) with some I/O (reading files). Guess which parallelization strategy will win, write it down, then measure.

### 2. The GIL: what it is, why it exists, what it protects

CPython uses **reference counting** for memory management: every object carries a count of references to it; when it hits zero the object is freed. Incrementing and decrementing that count from multiple threads simultaneously would corrupt it (a classic data race). The GIL is the mutex that prevents this: **a thread must hold the GIL to run Python bytecode.** One holder at a time. Every ~5 ms (`sys.getswitchinterval()`) the running thread is asked to release it so another can run.

Consequences you must be able to state precisely:

- **Pure-Python CPU-bound code does not speed up with threads.** Two threads tokenizing take *at least* as long as one — often longer, due to contention and cache effects. Beazley's 2010 talk shows a two-thread program running slower than a single thread and explains exactly why.
- **I/O releases the GIL.** Blocking calls in C (`read()`, `socket.recv()`, `time.sleep()`) drop the lock while waiting. That's why threads *do* speed up I/O-bound code.
- **C extensions can release it too.** numpy releases the GIL during large array operations; hashing, compression, and many others do as well. Threaded numpy code often scales.
- **The GIL does not make your code thread-safe.** It protects the *interpreter's* internals, not *your* invariants. `counter += 1` is read-modify-write across several bytecodes; a thread switch in the middle loses an increment. You still need `threading.Lock` for shared mutable state. (Individual dict/list operations are atomic *in CPython* — a fact you should know and never rely on.)

### 3. Threads in Python: the API and the hazards

`threading.Thread(target=fn, args=...)`, `.start()`, `.join()`. Shared memory by default — every thread sees the same objects. Coordination primitives: `Lock` (mutual exclusion; use `with lock:`), `RLock`, `Semaphore`, `Event`, `Condition`, and the thread-safe `queue.Queue` — the producer/consumer channel that lets you avoid most locks entirely.

The hazards are the classic ones: **races** (two threads update a `Counter` at once — you'll get a wrong total), **deadlocks** (two locks acquired in different orders), and the Python-specific one: threads can't be killed, so design them to check a stop flag or drain a queue.

The right abstraction for "run this function on these inputs in parallel" is not raw threads; it's the next section.

### 4. `concurrent.futures`: one API, two backends

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

with ProcessPoolExecutor(max_workers=8) as pool:
    futures = [pool.submit(build_partial_index, chunk) for chunk in chunks]
    for fut in as_completed(futures):
        merge_into(index, fut.result())
```

Swap `ProcessPoolExecutor` for `ThreadPoolExecutor` and *nothing else changes*. That's the point: same code, two execution models, so you can benchmark them against each other honestly. `pool.map(fn, items, chunksize=...)` is the simpler form when you want results in order. A **`Future`** is a handle to a result that isn't ready yet — `.result()` blocks; `as_completed` yields futures as they finish; `.exception()` gives you the error if the task raised.

The pool also handles the hard parts: a fixed number of workers, task queuing, exception propagation, and clean shutdown via the context manager.

### 5. Processes: what it costs to escape the GIL

Each worker process is a **separate interpreter** with its own memory. To run your function there, Python must **pickle** the function reference and its arguments, send them over a pipe, and pickle the result back. Three consequences:

- **Only picklable things can cross.** Module-level functions yes; lambdas and nested functions no; open files and locks no. Your `Posting` dataclasses pickle fine.
- **Data transfer is the tax.** Sending a 200 MB document list to 8 workers is 1.6 GB of pickling. Send *paths* (or a slice of a file, or a range of `doc_id`s) and let the worker read its own data. Return *compact* results — a partial index, not the raw tokens.
- **Startup isn't free.** The default **start method** matters: `fork` (Linux, fast, inherits parent memory, unsafe with threads — being phased out as default in 3.14), `spawn` (macOS/Windows default, starts a fresh interpreter, re-imports your module), `forkserver`. Under `spawn`, **everything that launches workers must be under `if __name__ == "__main__":`** or you'll recursively spawn forever. Read the [multiprocessing programming guidelines](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines) once.

Design pattern for indexing: **map-reduce**. Map: each worker builds a partial index over its chunk of documents. Reduce: the parent merges partial indexes (concatenate and sort postings lists per term). The merge is sequential — and it's the part **Amdahl's law** says will limit your speedup: if 20% of the work is unparallelizable, the maximum speedup is 5× no matter how many cores you add. Measure the merge separately; it's your ceiling.

Advanced: `multiprocessing.shared_memory` and numpy arrays backed by it let workers share large read-only data without copying — a Lab 8 tool.

### 6. Free-threaded Python: the GIL is now optional

[PEP 703](https://peps.python.org/pep-0703/) made the GIL removable. Python 3.13 shipped an experimental `python3.13t` build; 3.14 declared free-threading officially supported (no longer experimental). In this build, threads *do* run Python bytecode in parallel — CPU-bound threaded code scales with cores — at the cost of ~5–10% single-thread overhead and the requirement that C extensions be updated for thread safety (numpy and most major libraries now are).

You'll install it (`uv python install 3.13t` gets you the free-threaded build) and run your `ThreadPoolExecutor` indexer on it. Check `sys._is_gil_enabled()`. Watch the same code that didn't scale under the GIL suddenly scale. Then find the race condition it exposes in your code — because without the GIL's accidental serialization, the `Counter` you shared between threads *will* lose updates. That's the deepest lesson of this lab: the GIL was hiding your bugs.

The [py-free-threading guide](https://py-free-threading.github.io/) tracks ecosystem compatibility and explains the programming model.

### 7. Benchmarking honestly

- **Warm up** (first run pays import/JIT/cache costs). **Repeat** (≥ 3 runs, report median and spread). Use `time.perf_counter()`; `timeit` for micro-benchmarks.
- Report **wall-clock time** *and* **CPU time** (`time.process_time()` or `/usr/bin/time -v`). A process pool with 8 workers might show 8 s wall and 60 s CPU — that's the cost of coordination made visible.
- **Vary the worker count**: 1, 2, 4, 8, 16. Plot speedup vs. workers against the ideal line. Where it flattens is where Amdahl or memory bandwidth took over.
- Control the machine: close the browser, plug in the laptop, note the CPU model and core count in the README.

### Prove it to yourself (terminal, 15 minutes)

1. A CPU-bound function (`sum(i*i for i in range(10**7))`). Run it once; twice sequentially; twice in two threads; twice in two processes. Four timings. Explain each.
2. Two threads each doing `for _ in range(10**6): shared += 1` with a global `shared`. Final value? Add a `Lock`. Now?
3. `sys.getswitchinterval()`. Set it to `0.0001` and re-run experiment 1's threaded case. What changed and why?
4. Submit a lambda to `ProcessPoolExecutor`. Read the error. Now understand Section 5.
5. On `python3.13t`: `sys._is_gil_enabled()`, then experiment 1's threaded case again.

---

## Project step: parallel indexing

### Milestones

**M1 — Chunk the work; build partial indexes.**
Refactor `build_index` into `build_partial(doc_paths: list[Path]) -> PartialIndex` (a module-level, picklable function; returns compact postings) and `merge(partials: Iterable[PartialIndex]) -> Index` (sorted-merge of postings per term; `doc_id`s must be globally unique — assign ranges to chunks up front). Chunk by *paths*, not by loaded documents. The serial version is `merge([build_partial(all_paths)])` and must produce an index **identical** to Lab 4's — write a test that proves it.

**M2 — Three executors, one flag.**
`findex index --workers N --executor {serial,threads,processes}`. Same `build_partial`/`merge` code under `ThreadPoolExecutor`, `ProcessPoolExecutor`, or a plain loop. Everything that launches processes is under `if __name__ == "__main__"` (or the typer entry point, which is equivalent). Handle a worker exception so the whole build fails loudly with the original traceback, not a hang.

**M3 — The benchmark.**
On your full corpus, workers ∈ {1, 2, 4, 8, `os.cpu_count()`}, each configuration ≥ 3 runs. Record wall time, CPU time, peak memory of the parent, and the merge time separately. Produce:

| Executor | Workers | Wall (s, median) | CPU (s) | Peak RSS | Merge (s) | Speedup |
|---|---|---|---|---|---|---|
| serial | 1 | | | | | 1.0× |
| threads | 2 / 4 / 8 | | | | | |
| processes | 2 / 4 / 8 | | | | | |

Plus a speedup-vs-workers **plot** (matplotlib; a PNG in the README) with the ideal linear line for reference.

**M4 — Free-threaded run, and the explanation.**
Install `3.13t` via `uv`, run the `threads` configuration again, add the rows. Then write the section of the README this lab is really about — **one page, in your own words**: why threads didn't scale under the GIL, why processes did (and what they cost — look at CPU vs wall and at RSS), where Amdahl's law shows up in your merge time, and what changed on the free-threaded build. If the free-threaded run exposed a race (shared `Counter`, shared list), document the bug and the fix — that's a gold-star paragraph.

Bonus honesty: also parallelize a genuinely **I/O-bound** step (reading files off disk, or — foreshadowing Lab 6 — fetching 50 URLs) with threads and show that *there*, threads scale fine. Two benchmarks, one lesson.

### Definition of done

- Serial, threaded, and process-based indexing produce byte-identical indexes (tested).
- Benchmark table and speedup plot in the README, with machine specs and methodology.
- Free-threaded 3.13 row present; any exposed race documented and fixed.
- The one-page explanation covers GIL, I/O vs CPU-bound, pickling cost, Amdahl.
- `--executor processes` is the new default when it wins on your machine, and the code is `spawn`-safe.
- Repo tagged `lab-05`.

---

## Resources

**Watch**

- David Beazley — [Understanding the Python GIL (PyCon 2010, 45 min)](https://www.youtube.com/watch?v=Obt-vMVdM8s). The talk that made the GIL legible: what it is, how thread switching works, and the famous demonstration of two threads running *slower* than one. Still the best explanation fifteen years later; the 3.2 "new GIL" it discusses is what you're running.
- Raymond Hettinger — [Keynote on Concurrency (PyBay 2017, 1h)](https://www.youtube.com/watch?v=9zinZmE3Ogk). Threads vs processes vs async, when to use each, and a set of rules for writing correct threaded code (queue everything, lock nothing) that you should adopt wholesale.
- David Beazley — [Python Concurrency From the Ground Up: LIVE! (PyCon 2015, 45 min)](https://www.youtube.com/watch?v=MCs5OvhV9S4). Builds a server with threads, then with an event loop, then with coroutines — live, from nothing. The bridge between this lab and Lab 6. Watch it now; watch it again after Lab 6.

**Read**

- Real Python — [What Is the Python Global Interpreter Lock (GIL)?](https://realpython.com/python-gil/). The clearest written explanation, with the reference-counting motivation and a threads-vs-processes benchmark you should reproduce.
- Real Python — [Speed Up Your Python Program With Concurrency](https://realpython.com/python-concurrency/). I/O-bound vs CPU-bound, `threading` vs `asyncio` vs `multiprocessing`, with the same problem solved each way and timed. The structure of your M3 benchmark.
- Python docs — [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) and the [`multiprocessing` programming guidelines](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines) (read the guidelines, especially about start methods and `__main__`).
- [PEP 703 — Making the Global Interpreter Lock Optional in CPython](https://peps.python.org/pep-0703/). Read the Motivation and the Overview of the design; skip the implementation details unless they pull you in. Then the [Python 3.13 "What's New" section on free-threaded CPython](https://docs.python.org/3/whatsnew/3.13.html).
- [Python free-threading guide](https://py-free-threading.github.io/) — how to install, what's compatible, how to write code that's correct without the GIL.
- *Fluent Python*, 2nd ed. — Chapter 19 ("Concurrency Models in Python") and Chapter 20 ("Concurrent Executors").

---

## Deliverable checklist

- [ ] `build_partial` / `merge` split; serial and parallel builds produce identical indexes (test).
- [ ] `--executor {serial,threads,processes}` and `--workers N`; `spawn`-safe entry point; worker exceptions surface with tracebacks.
- [ ] Benchmark table (wall, CPU, RSS, merge time, speedup) for 1/2/4/8/all workers × 3 executors, ≥ 3 runs each, machine specs noted.
- [ ] Speedup-vs-workers plot PNG in the README.
- [ ] Free-threaded 3.13 row; race condition (if exposed) documented and fixed with a `Lock` or by removing shared state.
- [ ] One-page explanation: GIL, I/O vs CPU, pickling tax, Amdahl, free-threading.
- [ ] Optional I/O-bound counter-benchmark showing threads scale there.
- [ ] Git tag `lab-05`.

---

## Reflection — explain it at the whiteboard

1. What is the GIL, precisely — what does it lock, and why does CPython need it? What does it *not* protect?
2. Your threaded indexer at 8 workers was no faster (or slower) than serial. Walk through what the 8 threads were actually doing.
3. Your process-based indexer showed 8 s wall time and 45 s CPU time. Where did the extra 37 CPU-seconds go?
4. Why must the function you submit to a `ProcessPoolExecutor` be defined at module level? What happens with a lambda?
5. `fork` vs `spawn`: what does each do, what's the danger with `fork`, and why must the launch be under `if __name__ == "__main__"`?
6. State Amdahl's law. Your merge step is 15% of total serial time — what's the maximum speedup with infinite cores?
7. Why did the free-threaded build expose a bug that the normal build didn't? Is the code "correct" on the normal build?
8. `counter += 1` is not atomic. Show the bytecodes (`dis`) and where a thread switch loses an update.
9. Give one workload where threads are the right answer, one where processes are, one where neither is (→ Lab 6).

---

## Stretch

Share the read-only corpus text between workers with **`multiprocessing.shared_memory`** (or by `mmap`-ing the corpus file in each worker) and measure how much of the pickling tax disappears. Then try **sub-interpreters** (`concurrent.futures.InterpreterPoolExecutor`, Python 3.14) as a fourth executor: each sub-interpreter has its own GIL but lives in one process — cheaper than processes, isolated unlike threads. Add the row. You'll have benchmarked every concurrency model CPython offers on one real workload — a genuinely rare thing to have on a CV.
