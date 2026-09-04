# Lab 08 — Fast, Then Smart: Profiling, NumPy, and Semantic Search

> "Premature optimization is the root of all evil. So is never measuring."

**Weeks:** 15–16 · **Language focus:** profiling (`cProfile`, `py-spy`, Scalene), benchmarking methodology, why CPython is slow and NumPy is fast, vectorization and broadcasting, memory layout; embeddings and vector search · **Project step:** make the hot path measurably faster; optionally add hybrid keyword + semantic search; final polish and showcase · **Course:** [Python — Build a Search Engine](README.md) · **Previous:** [Lab 07](lab-07-fastapi-web-search.md)

---

## This lab's feature

Two things remain to make `findex` a project people remember. First, **speed** — not guessed, *measured*: find the three lines where the time actually goes, understand why CPython spends it there, and move that work into NumPy's compiled loops. Second, **intelligence** — the thing that makes a 2026 search engine different from a 1996 one: **embeddings**. Represent every document as a vector so that "how do I make Python faster" finds a document about *performance optimization* even if it never uses the word "faster." Then combine both signals — this is **hybrid search**, and it's what modern retrieval systems (including the RAG pipelines behind LLM applications, [Lab 31](../../labs/lab-31-llm-rag-app.md)) actually do.

Both halves rest on the same idea: **Python is a great language for orchestrating fast code written elsewhere.** NumPy is that code for arrays; a sentence-embedding model is that code for meaning. Learning when to stop writing Python loops and start calling into compiled kernels is the last big Python skill, and the one that separates the people who say "Python is slow" from the people who ship fast Python.

---

## Theory

### 1. Measure first: the profiling toolbox

Optimizing without a profile is guessing, and the guesses are usually wrong. Three tools, each answering a different question:

- **[`cProfile`](https://docs.python.org/3/library/profile.html)** — *deterministic*: instruments every function call. `python -m cProfile -o out.prof -m findex search ...`, then `snakeviz out.prof` for a sunburst, or `pstats` sorted by `cumtime`. Tells you **which functions** account for the time. Overhead is significant, so don't trust absolute numbers — trust the ranking.
- **[`py-spy`](https://github.com/benfred/py-spy)** — *sampling*: attaches to a running process (even production, even inside Docker) and records what's on the stack a few hundred times a second. Near-zero overhead; produces **flame graphs** (`py-spy record -o profile.svg -- python -m findex ...`) and a live `top`. Tells you **where the time really goes** without distortion, and can show you native frames (`--native`) when the time is inside NumPy or a C library.
- **[Scalene](https://github.com/plasma-umass/scalene)** — line-level CPU *and* memory profiler that separates *Python time* from *native time* from *system time* per line. If a line is 90% native, Python-level optimization won't help it; if it's 90% Python, it's a vectorization candidate. Emery Berger's talk explains why this split is the number you actually need.

For memory specifically: [`memray`](https://github.com/bloomberg/memray) (allocation flame graphs) and `tracemalloc` (Lab 1).

The process: profile → find the top 3 hotspots → hypothesize → change one thing → **benchmark** → keep or revert. Benchmarking rules from Lab 5 apply: warm up, repeat, report median and spread, control the machine; [`pytest-benchmark`](https://pypi.org/project/pytest-benchmark/) turns benchmarks into tests that fail if you regress.

### 2. Why CPython is slow (and when it isn't)

Anthony Shaw's talk answers the title question honestly. CPython interprets bytecode: every `a + b` involves a dispatch loop, a type check on both operands, a lookup of `__add__`, boxing the result into a new heap-allocated `PyObject`, and reference-count updates — dozens of machine instructions for what C does in one. Attribute access is a dict lookup (Lab 2). A `for` loop over a million floats does all of this a million times.

None of that matters when the time is spent *elsewhere*: waiting on I/O (Lab 6), inside a C extension, or in an algorithm whose complexity is wrong. So the first question is always algorithmic — you don't vectorize an O(n²) loop, you replace it — and the second is "is the time actually in Python-level code?" (Scalene tells you). Only then does Section 3 apply. Also note: CPython 3.11–3.13 got substantially faster (specializing adaptive interpreter, PEP 659), and 3.13+ ships an experimental JIT; the gap is narrowing, but the model still holds.

### 3. NumPy: move the loop into C

A NumPy array is a **contiguous block of raw numbers** with a dtype and a shape — not a list of Python objects. `arr * 2.0` runs a single compiled loop over that block: no dispatch, no boxing, no reference counting, and often SIMD. That is where the 100× comes from. Jake VanderPlas's talk gives the four strategies, which are the whole skill:

1. **ufuncs** — element-wise operations (`+`, `np.log`, `np.maximum`) on whole arrays. Never `for x in arr`.
2. **Aggregations** — `arr.sum()`, `.max()`, `.argmax()`, along an `axis`.
3. **[Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)** — combining arrays of different shapes by stretching dimensions of size 1: a `(N, 1)` column times a `(1, M)` row gives an `(N, M)` outer product with no loop and no copy.
4. **Fancy indexing and masking** — `arr[idx_array]`, `arr[arr > 0]`, `np.argpartition` for top-k in O(n) instead of a full sort.

Applied to BM25: your postings for a term are a `doc_ids: int32[n]` array and a `tfs: int32[n]` array (Lab 2's `array('I')` was the warm-up; `np.frombuffer` turns it into a NumPy view *without copying*). The score for all `n` documents at once is one expression:

```python
idf = np.log(1 + (N - df + 0.5) / (df + 0.5))
norm = k1 * (1 - b + b * doc_len[doc_ids] / avg_len)         # fancy indexing into doc_len
scores[doc_ids] += idf * tfs * (k1 + 1) / (tfs + norm)       # ufuncs + scatter-add
```

No Python loop over documents. For a query with 3 terms and 50,000 matching documents, that's three array expressions instead of 150,000 iterations of Lab 3's loop. Then `np.argpartition(scores, -k)[-k:]` for the top-k.

Memory layout matters: `int32` over `int64` halves the bytes; contiguous arrays stream through the cache; `np.memmap` lets the postings live on disk and be paged in on demand — Lab 2's Stretch, now with a real payoff.

When NumPy isn't enough: Numba (JIT-compile a Python function), Cython, or Rust via PyO3/maturin. Know they exist; you probably won't need them here.

### 4. Embeddings: meaning as geometry

An **embedding model** is a neural network that maps a piece of text to a vector — typically 384 to 1,024 floats — such that texts with similar *meaning* land near each other. "How do I speed up my code" and "Python performance optimization" share no keywords and sit close together anyway. Vicki Boykis's free book [*What Are Embeddings*](https://vickiboykis.com/what_are_embeddings/) is the best gentle-but-rigorous introduction; you don't need to know how the model was trained to use it well.

Practicalities:

- **Model**: [`sentence-transformers`](https://www.sbert.net/) with a small model such as `all-MiniLM-L6-v2` (384 dimensions, ~80 MB, runs fine on CPU, embeds ~1,000 sentences/s). Multilingual models (`paraphrase-multilingual-MiniLM-L12-v2`) handle Ukrainian and English in one space — pick one if your corpus is Ukrainian. An API (OpenAI, Voyage, Cohere) is an alternative if you'd rather not run a model.
- **Chunking**: embed **passages** (~200–500 tokens), not whole documents — a 40-page document's single vector is mush. Store `(doc_id, chunk_id, vector)`; a document's score is its best chunk's score.
- **Similarity**: **cosine** — normalize every vector to unit length once, then similarity is a dot product. For a query vector `q` and an `(N, d)` matrix `E` of normalized chunk vectors, `E @ q` gives all `N` similarities in one matrix-vector product. That is brute-force vector search, and for anything under a few hundred thousand chunks it's *fast enough* — a few milliseconds. This is NumPy earning its place.
- **Scale**: past ~10⁶ vectors you need an **approximate nearest-neighbor** index — HNSW in [FAISS](https://github.com/facebookresearch/faiss), `hnswlib`, or a vector database. Know the name; don't reach for it until brute force is actually slow.

### 5. Hybrid search: combining two rankings

Keyword search (BM25) is precise — exact terms, names, code identifiers, rare words — and brittle to vocabulary mismatch. Semantic search is the reverse. Production systems run **both** and fuse the rankings. The simplest robust method is **Reciprocal Rank Fusion** ([RRF](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html)): each document's fused score is `Σ 1 / (k + rank_i)` over the lists it appears in, with `k ≈ 60`. No score normalization needed, hard to get wrong, and consistently competitive. Implement it in ten lines; expose `?mode=keyword|semantic|hybrid`.

Then **evaluate**, the Lab 3 way: your 10 labeled queries, precision@5 for each mode — plus, importantly, **add 5 queries that use different words than the documents** (paraphrases). Watch keyword search fail on those and semantic search catch them. That table, with a paragraph of interpretation, is the strongest thing in your final README.

### 6. Finishing a project

The last week is for making the project *legible to a stranger in 90 seconds*. In order of impact:

1. **The README's first screen**: one sentence on what it is, the **live URL**, a **GIF** of a search happening, and the three most impressive numbers (corpus size, p95 latency, the biggest speedup you achieved).
2. **An architecture diagram** (Mermaid is fine): corpus → crawler → tokenizer → index → scorer → API → UI, with the lab number where each piece was built.
3. **The measurements**, collected in one place: every table you built in Labs 1–8. Together they tell a story no tutorial project has.
4. **Honest limitations and next steps.** Reviewers trust people who know what their software doesn't do.
5. A **2–3 minute demo video** (screen recording, your voice) linked at the top. This is what actually gets watched.

The [portfolio guidance in Lab 15](../../labs/lab-15-mini-search-engine.md) and the [root README](../../README.md) apply in full.

### Prove it to yourself (terminal, 15 minutes)

1. `python -m cProfile -s cumtime -m findex search index.bin "your query"` — what are the top 3 functions by cumulative time? Did you guess right?
2. `py-spy record -o p.svg -- python -m findex index data/` — open the SVG. Find the widest bar that's *your* code.
3. `%timeit sum(x*x for x in range(10**6))` vs `%timeit (np.arange(10**6)**2).sum()`. Ratio? Now with `10**2` — why does NumPy lose?
4. `a = np.arange(5)[:, None]; b = np.arange(3)[None, :]; (a * b).shape` — explain the shape without running it, then run it.
5. Embed `"the cat sat on the mat"`, `"a feline rested on the rug"`, and `"the stock market fell"` with `all-MiniLM-L6-v2`; compute the three pairwise cosine similarities. Do the numbers match your intuition?

---

## Project step: fast, then smart, then finished

### Milestones

**M1 — Profile and pick the targets.**
Profile `findex index` and `findex search` (a 3-term query on your full corpus) with `cProfile` *and* `py-spy`. Include the flame graph SVG in `docs/`. Identify the **top 3 hotspots** by real time and, using Scalene, whether each is Python-time or native-time. Write them down *before* changing anything, with a hypothesis for each. Set up `pytest-benchmark` for `search` and `build_index` on the fixture corpus so regressions fail CI.

**M2 — Vectorize the scorer.**
Store postings as NumPy arrays (`int32` `doc_ids`, `int32` `tfs`, built via `np.frombuffer` from Lab 2's arrays or directly); `doc_len` as one `int32[N]` array. Rewrite BM25 and TF-IDF as array expressions (Section 3) with `np.argpartition` top-k. **The ranking must be identical** to Lab 3's — a test compares the two on the fixture corpus. Then the table:

| Query | Docs matched | Lab 3 scorer (ms) | NumPy scorer (ms) | Speedup |
|---|---|---|---|---|
| common term | | | | |
| rare term | | | | |
| 3-term query | | | | |

Explain the speedups — and where it's small, explain that too (small postings lists don't benefit; Python-call overhead dominates). Optionally `np.memmap` the postings and report load time vs. Lab 2.

**M3 — Semantic and hybrid search (optional but strongly encouraged).**
`findex embed <index> --model all-MiniLM-L6-v2` chunks every document, embeds the chunks (with a `rich` progress bar; this takes minutes, not hours, on CPU), L2-normalizes, and saves `E: float32[N_chunks, d]` plus a chunk→doc map as `.npy`. `search(mode="semantic")` embeds the query and does `E @ q` → top chunks → best-chunk-per-doc. `search(mode="hybrid")` runs both and fuses with RRF. Expose `mode` in the CLI and the API/UI (a toggle on the search page). Evaluate: precision@5 for keyword / semantic / hybrid on your 10 original queries **plus 5 paraphrase queries**, in one table with interpretation.

If you skip M3: instead go deep on M2 — `memmap` postings, gap-encoded compressed postings decoded with NumPy, and a benchmark at 10× corpus size.

**M4 — Finish.**
The README rewrite from Section 6: first screen with live URL, GIF, headline numbers; architecture diagram; the consolidated measurements section (Labs 1–8); limitations; a 2–3 minute demo video. Update the deployed instance to `v1.0.0`. Tag `lab-08` and `v1.0.0`. Prepare your 5-minute showcase: the live demo, one measurement you're proud of, one bug that taught you something.

### Definition of done

- Flame graph in `docs/`; top-3 hotspots documented with hypotheses before and outcomes after.
- NumPy scorer produces identical rankings (tested) with a speedup table and explanation; `pytest-benchmark` in CI.
- Either semantic + hybrid search with the 15-query evaluation table, or the deep-optimization alternative with its benchmarks.
- README rewritten for a stranger: live URL, GIF, headline numbers, architecture diagram, all measurements, limitations, demo video.
- Deployed `v1.0.0`; tags `lab-08` and `v1.0.0`.

---

## Resources

**Watch**

- Jake VanderPlas — [Losing Your Loops: Fast Numerical Computing with NumPy (PyCon 2015, 30 min)](https://www.youtube.com/watch?v=EEUXKG97YRw). The four strategies (ufuncs, aggregations, broadcasting, fancy indexing) with timings. Section 3 is a summary of this talk; watch it before M2.
- Anthony Shaw — [Why Is Python Slow? (PyCon 2020, 30 min)](https://www.youtube.com/watch?v=I4nkgJdVZFA). By the author of *CPython Internals*: what the interpreter does per operation, and which "slow" claims are true. Section 2.
- Emery Berger — [Python Performance Matters (Strange Loop 2022, 40 min)](https://www.youtube.com/watch?v=vVUnCXKuNOg). Why separating Python-time from native-time is the profile you need, from the creator of Scalene. Also a fine tour of profiling methodology in general.

**Read**

- NumPy docs — [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html) (skim; you know most of it) and [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) (read carefully; it's the one rule everyone gets wrong).
- Python docs — [The Python Profilers](https://docs.python.org/3/library/profile.html) (`cProfile`, `pstats`); [`py-spy` README](https://github.com/benfred/py-spy); [Scalene README](https://github.com/plasma-umass/scalene); [`memray`](https://github.com/bloomberg/memray).
- Itamar Turner-Trauring — [pythonspeed.com](https://pythonspeed.com/). Dozens of short, precise articles on Python and NumPy performance and memory. Browse the "Performance" and "Memory" sections.
- Vicki Boykis — [*What Are Embeddings*](https://vickiboykis.com/what_are_embeddings/). A free, ~80-page book: history, intuition, and enough math. Chapters 1–3 for this lab.
- [Sentence-Transformers documentation](https://www.sbert.net/) — quick start, "Semantic Search," and the pretrained model table (pick by size/speed/language).
- Pinecone — [Learning Center](https://www.pinecone.io/learn/): the "Vector Search" and "Hybrid Search" series are clear, vendor-agnostic explanations. Elastic — [Reciprocal Rank Fusion](https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html) for the RRF formula and rationale.
- [FAISS](https://github.com/facebookresearch/faiss) — for when brute force isn't enough; read the wiki's "Getting started" to know what's there.
- *Fluent Python*, 2nd ed. — Chapter 2, section on NumPy and memory views; and the *CPython Internals* book (Anthony Shaw) if Section 2 pulled you in.

---

## Deliverable checklist

- [ ] `cProfile` + `py-spy` profiles of `index` and `search`; flame graph SVG in `docs/`; top-3 hotspots with Python-vs-native breakdown and hypotheses.
- [ ] Postings as NumPy `int32` arrays; BM25/TF-IDF vectorized; `np.argpartition` top-k; identical-ranking test passes.
- [ ] Speedup table (≥ 3 queries) with explanation, including where the speedup was small and why.
- [ ] `pytest-benchmark` tests in CI for `search` and `build_index`.
- [ ] (M3) `findex embed`; `mode=keyword|semantic|hybrid` in CLI, API, and UI; RRF fusion; 15-query precision@5 table with paraphrase queries and interpretation. *Or* the deep-optimization alternative with benchmarks.
- [ ] README: live URL, GIF, headline numbers, architecture diagram, consolidated measurements (Labs 1–8), limitations, demo video.
- [ ] Deployed `v1.0.0`; git tags `lab-08`, `v1.0.0`.
- [ ] 5-minute showcase prepared.

---

## Reflection — explain it at the whiteboard

1. `cProfile` vs `py-spy` vs Scalene: what does each measure, how, and which one do you attach to a production process?
2. Walk through what CPython does to evaluate `a + b` for two floats. Now what NumPy does for `A + B` on two million-element arrays. Where did the 100× come from?
3. Explain broadcasting with a `(N, 1)` and a `(1, M)` array. What shape results, and how much memory does the intermediate use?
4. Why `np.argpartition` rather than `np.argsort` for top-k? Complexity of each?
5. Your speedup was 40× on the common term and 1.5× on the rare one. Why?
6. What is an embedding? Why cosine similarity, and why can you replace it with a dot product after normalization?
7. Why embed chunks rather than whole documents? What does "best chunk per document" fix?
8. Explain RRF. Why is it preferred over adding the two raw scores together?
9. Show your 15-query table. Which queries did keyword search lose, which did semantic lose, and what does hybrid's result tell you?
10. If your corpus grew to 50 million chunks, what breaks first in your design, and what would you reach for?

---

## Stretch

Replace brute-force `E @ q` with an **HNSW index** (FAISS or `hnswlib`) and measure recall@10 against brute force at several `ef` values — the precision/speed trade-off of approximate search, quantified. Then make the embedding step **incremental** (only new/changed chunks) and run it as a background job from the Lab 7 API. Finally, close the loop with [Lab 31](../../labs/lab-31-llm-rag-app.md): put an LLM on top of your hybrid retriever so `findex ask "how does the scheduler work?"` returns an answer *with citations to your own documents*. Your search engine is now a RAG system — and you built every layer of it yourself.
