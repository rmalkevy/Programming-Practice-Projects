# Lab 03 — Ranking and the Object Model: Dunder Methods, Protocols, Decorators

> "Everything is an object, and every object can be taught to behave like a built-in."
> — the Python data model, paraphrased

**Weeks:** 5–6 · **Language focus:** the data model (dunder methods), properties, protocols and duck typing, closures and decorators, `functools`, context managers · **Project step:** TF-IDF / BM25 ranking, a real query language, snippets, and a clean `Index` API · **Course:** [Python — Build a Search Engine](README.md) · **Previous:** [Lab 02](lab-02-data-structures-and-the-inverted-index.md)

---

## This lab's feature

Your index is a bag of dicts and functions. It works, but `len(index)` fails, `"python" in index` fails, and every caller has to know the dict layout. This lab is about turning it into an *object that behaves like Python* — one you can `len()`, iterate, index, compare, print, and `with` — by implementing the **special methods** the language calls behind your back.

This is the **data model**, and it's what makes Python feel like Python. `len(x)` calls `x.__len__()`. `x in y` calls `y.__contains__(x)`. `with x:` calls `__enter__`/`__exit__`. `@decorator` is a function call. Once you see the mechanism, the language stops being a set of built-in magic and becomes a set of protocols you can join. Fluent Python opens with this chapter for a reason.

Meanwhile the search engine grows up: Boolean matching becomes **ranking** (TF-IDF, then BM25 — the algorithm behind Lucene, Elasticsearch, and most of the web before neural search), `a AND (b OR c) NOT d "exact phrase"` becomes a parsed query, and results get snippets.

---

## Theory

### 1. Special methods: how built-ins dispatch to your code

Every operator and built-in function in Python is a thin wrapper over a "dunder" (double-underscore) method call. The interpreter does the call; you implement the method. The ones you'll use this lab:

| You write | Python calls | Use in `findex` |
|---|---|---|
| `len(index)` | `index.__len__()` | number of terms |
| `"python" in index` | `index.__contains__("python")` | is the term indexed? |
| `index["python"]` | `index.__getitem__("python")` | postings list (raise `KeyError` if absent) |
| `for term in index` | `index.__iter__()` | iterate terms |
| `repr(index)` / in the REPL | `index.__repr__()` | `Index(terms=48_211, docs=3_402)` |
| `str(result)` / `print(result)` | `result.__str__()` (falls back to `__repr__`) | pretty result line |
| `a == b` | `a.__eq__(b)` | compare documents/postings |
| `a < b`, `sorted(results)` | `a.__lt__(b)` | order results by score |
| `q1 & q2`, `q1 \| q2`, `~q` | `__and__`, `__or__`, `__invert__` | compose queries as objects |
| `scorer(term, doc)` | `scorer.__call__(term, doc)` | make a scorer behave like a function |
| `with open_index(p) as ix:` | `__enter__` / `__exit__` | load + guaranteed cleanup |
| `bool(results)` | `__bool__` (else `__len__`) | `if results:` |
| `hash(posting)` | `__hash__` | Lab 2 |

Rules of the road: implement `__repr__` on *every* class (debugging is 10× easier — aim for output that could recreate the object); `__eq__` should return `NotImplemented` for foreign types, not `False`; `__lt__` plus `@functools.total_ordering` gives you all six comparisons; never call dunders directly in normal code (`len(x)`, not `x.__len__()`) — the built-in does extra work (type checks, fast paths for C types).

### 2. Protocols and duck typing: "behaves like" beats "is a"

Python doesn't ask "is this a `Sequence`?" — it asks "does this respond to `__len__` and `__getitem__`?" An object that implements the right methods *is* a sequence for every practical purpose. This is **duck typing**, and the sets of methods that define behaviors are **protocols**: iterable (`__iter__`), sized (`__len__`), container (`__contains__`), callable (`__call__`), context manager (`__enter__`/`__exit__`).

You can make this explicit in two ways:

- **`collections.abc`** — inherit from `Mapping` or `Sequence` and implement only the abstract methods (`__getitem__`, `__len__`, `__iter__`); you get `keys()`, `items()`, `get()`, `__contains__` and more for free, correctly. Your `Index` may well be a `Mapping[str, list[Posting]]`.
- **`typing.Protocol`** (Lab 4 formalizes this) — declare an interface structurally: any object with a matching `score(term, doc) -> float` method satisfies `Scorer` without inheriting from it. This is how you'll swap TF-IDF and BM25.

The design principle: **prefer composition and protocols over inheritance hierarchies**. A `Scorer` protocol with two independent implementations beats a `BaseScorer` class with subclasses.

### 3. Properties: computed attributes, no getters

Java-style `get_score()` is un-Pythonic. If a value is derived, expose it as an attribute and compute it on access:

```python
class Index:
    @property
    def num_docs(self) -> int:
        return len(self._doc_lengths)

    @functools.cached_property
    def avg_doc_length(self) -> float:      # computed once, then cached on the instance
        return sum(self._doc_lengths.values()) / self.num_docs
```

`@property` is a **descriptor** — an object whose `__get__` runs when you access the attribute. Descriptors are also how methods bind `self`, how `@classmethod` and `@staticmethod` work, and how ORMs define fields. You don't need to write your own this lab, but read the [Descriptor HOWTO](https://docs.python.org/3/howto/descriptor.html) once so `property` stops being magic.

`cached_property` matters here: `avg_doc_length` is needed by BM25 on every scored document; computing it once per index, not once per document, is the difference between fast and unusable.

### 4. Closures and decorators: functions that wrap functions

A **closure** is a function that remembers variables from the scope it was created in, even after that scope is gone:

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc
```

A **decorator** is a function that takes a function and returns a (usually wrapped) function. `@timed` above `def search` is exactly `search = timed(search)`. Nothing more:

```python
import functools, time

def timed(fn):
    @functools.wraps(fn)                  # copies __name__, __doc__, etc. onto the wrapper
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - t0
            log.debug("%s took %.1f ms", fn.__name__, elapsed * 1000)
    return wrapper
```

Three things people get wrong: forgetting `functools.wraps` (then `search.__name__` is `"wrapper"` and your docs/tests break); decorators **with arguments** need one more level (`def retry(times): def decorator(fn): def wrapper(...)`); and class-based decorators (any object with `__call__`) are sometimes cleaner when the decorator needs state.

`functools` is the decorator toolbox: `lru_cache` / `cache` (memoize by arguments — perfect for repeated queries; note it requires hashable args), `partial` (pre-fill arguments), `singledispatch` (overload on the type of the first argument), `total_ordering`, `wraps`, `cached_property`.

### 5. Context managers: guaranteed cleanup

`with` guarantees that `__exit__` runs, whether the block finishes, `return`s, or raises. It's Python's answer to RAII / `try/finally`. Two ways to write one:

```python
class open_index:
    def __init__(self, path): self.path = path
    def __enter__(self):
        self.index = load(self.path); return self.index
    def __exit__(self, exc_type, exc, tb):
        self.index.close(); return False      # False = don't swallow exceptions

# or, with a generator: everything before `yield` is __enter__, everything after is __exit__
from contextlib import contextmanager

@contextmanager
def open_index(path):
    index = load(path)
    try:
        yield index
    finally:
        index.close()
```

The generator form is Lab 1's `yield` doing a completely different job — that's the "generators are a control-flow primitive" insight from Beazley's talks. Also in `contextlib`: `suppress`, `redirect_stdout`, `ExitStack` (manage a dynamic number of context managers), and `closing`.

### 6. Ranking: from matching to scoring

Boolean search returns a *set*. Users want a *ranked list*. The classic ideas ([IR book, Chapter 6](https://nlp.stanford.edu/IR-book/html/htmledition/scoring-term-weighting-and-the-vector-space-model-1.html)):

- **TF** — a term that appears 10 times in a document is more "about" it than one appearing once. But 10 vs 1 isn't 10× more relevant — use `1 + log(tf)` or the saturation below.
- **IDF** — a term appearing in 3 documents out of 100,000 is far more informative than "the." `idf(t) = log(N / df(t))`. Rare terms weigh more.
- **TF-IDF** — `score(q, d) = Σ_t∈q tf(t, d) · idf(t)`. Simple, effective, the 1970s baseline everyone still uses.
- **BM25** — TF-IDF with two fixes: **term-frequency saturation** (the 11th occurrence adds almost nothing; controlled by `k1 ≈ 1.2–2.0`) and **document-length normalization** (a long document matching once is less relevant than a short one; controlled by `b ≈ 0.75`). The [Elastic "Practical BM25"](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables) post derives every term in the formula in plain language; [Wikipedia](https://en.wikipedia.org/wiki/Okapi_BM25) has the formula itself. BM25 is the default in Lucene/Elasticsearch and remains a strong baseline that neural methods are measured against.

Implementation: for each query term, walk its postings, accumulate `score[doc_id] += weight` in a dict, then take the top-k with `heapq.nlargest(k, scores.items(), key=itemgetter(1))` — O(n log k), not a full sort.

### 7. Parsing the query

`python AND (async OR await) NOT java "event loop"` needs a small **recursive-descent parser**: tokenize → parse `or_expr → and_expr ('OR' and_expr)*` → `and_expr → not_expr ('AND'? not_expr)*` → `not_expr → 'NOT' atom | atom` → `atom → term | phrase | '(' or_expr ')'`. It's forty lines and one of the most useful things a programmer can know how to write.

Represent the parsed query as **objects that overload operators**: `Term("python") & (Term("async") | Term("await")) & ~Term("java")`. Each node has `.evaluate(index) -> set[doc_id]` (or a postings stream). Now the parser's job is just to build that tree — and you can construct queries programmatically in tests without any string at all.

**Phrase queries** use the positions you (maybe) stored in Lab 2: two terms form a phrase in doc `d` if some position `p` of the first has `p + 1` in the positions of the second. Two-pointer merge again, on positions this time.

### Prove it to yourself (REPL, 10 minutes)

1. `class V: pass` — `len(V())` fails. Add `__len__` returning 3. Now `len(V())`, and `bool(V())` — why is the second `True`?
2. Write `@timed` without `functools.wraps`. Check `search.__name__` and `help(search)`. Add `wraps`. Check again.
3. `import dis; dis.dis(lambda: len(x))` — find the `CALL` that becomes `__len__`. Now `dis.dis(lambda: x.__len__())` — why is the first faster in C types?
4. `@functools.lru_cache` on a function taking a `list`. Call it. Read the error. Now pass a `tuple`.
5. Write a `@contextmanager` that prints on enter and exit. `return` from inside the `with` body. Did exit print? Raise inside the body — did it?

---

## Project step: ranking, query language, and a real `Index`

### Milestones

**M1 — `Index` becomes an object.**
Refactor Lab 2's dicts into an `Index` class that implements `__len__` (terms), `__contains__`, `__getitem__` (postings, `KeyError` if absent), `__iter__`, `__repr__`, and exposes `num_docs`, `avg_doc_length` (`cached_property`), `doc_length(doc_id)`, `df(term)`. Consider inheriting `collections.abc.Mapping`. Add `open_index(path)` as a context manager. `Posting`/`DocMeta` stay as your Lab 2 dataclasses. Everything from Lab 2 still works, now through the object.

**M2 — Scoring with a swappable `Scorer`.**
A `Scorer` protocol: `score(term: str, posting: Posting, index: Index) -> float`. Two implementations: `TfIdf` and `BM25(k1=1.5, b=0.75)` — as classes with `__call__`, or plain functions; the protocol doesn't care. `search(query, scorer=BM25(), k=10)` accumulates scores per doc and returns the top-`k` via `heapq.nlargest`. Results are `SearchResult(doc_id, score, title)` dataclasses with `order=True` so `sorted(results)` works.

Sanity checks you must show: a document containing a rare query term outranks one containing only a common one; with BM25, the 20th repetition of a term adds almost nothing; a short document with one match outranks a very long one with one match. Show all three on your corpus.

**M3 — Query language.**
`query.py` — the recursive-descent parser producing a tree of `Term`, `Phrase`, `And`, `Or`, `Not` nodes; nodes overload `&`, `|`, `~`; each node has `evaluate(index)`. Syntax: implicit AND between terms, `OR`, `NOT`, parentheses, `"quoted phrases"`. Phrase queries require positions — if you skipped them in Lab 2, add them now (behind the flag). Ranking then applies to the matched set.

Write the parser tests as *trees*, not strings: `parse('a OR b c') == Or(Term('a'), And(Term('b'), Term('c')))`. That's what `__eq__` on dataclasses buys you.

**M4 — Decorators, caching, snippets, and a small evaluation.**
- `@timed` decorator (logs elapsed ms) on `search`, `build`, `load`.
- `@functools.lru_cache(maxsize=256)` on the query → result-ids path. Show the hit on a repeated query in the timing log.
- **Snippets:** for each result, extract a ±80-character window around the best-matching position and **highlight** the matched terms. Positions make this trivial; without them, `str.find` on the casefolded text works.
- **Evaluation:** write 10 queries you know the answer to for your corpus, hand-label the "should be in the top 5" documents, and compute **precision@5** for TF-IDF vs. BM25. Put the table in the README. It'll be small and noisy — that's fine; the habit of measuring ranking is the point.

### Definition of done

- `len(index)`, `term in index`, `index[term]`, `for t in index`, `repr(index)` all work; `with open_index(p) as ix:` works.
- TF-IDF and BM25 are interchangeable via the `Scorer` protocol; the three sanity checks are demonstrated.
- The query language handles AND/OR/NOT/parentheses/phrases; the parser has tree-equality tests.
- `@timed` and `lru_cache` are in use with evidence in logs; snippets highlight matches.
- precision@5 table for both scorers in the README.
- Repo tagged `lab-03`.

---

## Deliverable checklist

- [ ] `Index` implements `__len__`, `__contains__`, `__getitem__`, `__iter__`, `__repr__`; `num_docs`, `avg_doc_length` (`cached_property`), `df`.
- [ ] `open_index` is a context manager (either style), and resources are released on exceptions.
- [ ] `Scorer` protocol; `TfIdf` and `BM25` implementations; `heapq.nlargest` for top-k.
- [ ] Three ranking sanity checks demonstrated on your corpus in the README.
- [ ] Recursive-descent query parser; `Term`/`Phrase`/`And`/`Or`/`Not` nodes with `&`, `|`, `~`; tree-equality tests.
- [ ] `@timed` (with `functools.wraps`) and `lru_cache` in use; a repeated-query cache hit is visible in the log.
- [ ] Snippets with highlighted terms.
- [ ] precision@5 table (10 hand-labeled queries) for TF-IDF vs. BM25.
- [ ] Git tag `lab-03`.

---

## Reflection — explain it at the whiteboard

1. What happens, step by step, when Python evaluates `"python" in index`? And `len(index)`? Why should you never call `index.__len__()` directly?
2. What is a protocol in Python? How does `typing.Protocol` differ from an ABC, and when would you use each?
3. Write `@timed` from memory, including `functools.wraps`. What breaks without it?
4. How does a decorator *with arguments* differ structurally from one without? Sketch `@retry(times=3)`.
5. `@contextmanager` uses `yield`. What runs before the `yield`, what after, and what happens if the `with` body raises?
6. Explain BM25's two improvements over TF-IDF. What do `k1` and `b` control, and what happens at `b = 0`?
7. Why `heapq.nlargest(k, ...)` instead of `sorted(...)[:k]`? Complexity of each?
8. Show your parser handling `a OR b c`. Why is it `Or(a, And(b, c))` and not `And(Or(a, b), c)`?

---

## Stretch

Implement **`__getitem__` with slicing semantics** on your result list (so `results[:5]` works and returns a `ResultList`, not a plain list), then make `ResultList` a proper `collections.abc.Sequence`. Then implement a **`singledispatch`-based `explain(node)`** that pretty-prints any query tree node — and an `explain(scorer, doc)` that shows *why* a document got its score, term by term, the way Elasticsearch's `_explain` API does. A ranking you can explain is a ranking you can debug.

---

## Resources

**Watch**

- Raymond Hettinger — [Python's Class Development Toolkit (PyCon 2013, 45 min)](https://www.youtube.com/watch?v=HTLu2DFOdTg). Live-builds a class the Pythonic way: `__init__`, `__repr__`, properties, class methods, `__slots__`, and when each is warranted. The best 45 minutes on writing classes in Python.
- Raymond Hettinger — [Beyond PEP 8: Best Practices for Beautiful Intelligible Code (PyCon 2015, 50 min)](https://www.youtube.com/watch?v=wf-BqAjZb8M). Takes Java-flavored Python and transforms it using the data model — dunder methods, properties, context managers, named tuples. Watch this before refactoring `Index`.
- James Powell — [So You Want to Be a Python Expert? (PyData 2017)](https://www.youtube.com/watch?v=cKPlPJyQrt4) — the data model, decorators, and context managers segments (you watched the generators part in Lab 1). Live-coded from the ground up.
- Corey Schafer — [Decorators: Dynamically Alter the Functionality of Your Functions (30 min)](https://www.youtube.com/watch?v=FsAPt_9Bf3U). Closures → decorators → decorators with arguments → `wraps`, step by step, with a logging/timing example that is your `@timed`.

**Read**

- Python docs — [Data Model reference, §3.3 "Special method names"](https://docs.python.org/3/reference/datamodel.html). The authoritative list of every dunder and exactly when it's called. Skim it once; return to it forever.
- Real Python — [Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/). Long, thorough, and covers every pattern including class decorators and stateful decorators.
- Python docs — [Descriptor HOWTO](https://docs.python.org/3/howto/descriptor.html) by Raymond Hettinger. How `property`, methods, `classmethod` and `staticmethod` actually work. Read the first half.
- Python docs — [`functools`](https://docs.python.org/3/library/functools.html) and [`contextlib`](https://docs.python.org/3/library/contextlib.html). Reference pages you should know exist.
- Elastic — [Practical BM25, Part 2: The BM25 Algorithm and Its Variables](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables). The gentlest correct derivation of BM25, term by term, with intuition for `k1` and `b`.
- Manning, Raghavan & Schütze — [IR book, Chapter 6: Scoring, term weighting and the vector space model](https://nlp.stanford.edu/IR-book/html/htmledition/scoring-term-weighting-and-the-vector-space-model-1.html), and Chapter 2 for phrase queries and positional indexes.
- *Fluent Python*, 2nd ed. — Chapter 1 ("The Python Data Model"), Chapter 9 ("Decorators and Closures"), Chapter 12 ("Special Methods for Sequences"), Chapter 13 ("Interfaces, Protocols, and ABCs").
