# Lab 02 — The Inverted Index: Dictionaries, Hashing, and Memory

> "Python's dictionaries are stunningly good."
> — Raymond Hettinger, CPython core developer

**Weeks:** 3–4 · **Language focus:** `dict` and `set` internals, the hashing contract, `collections`, `dataclasses`, `__slots__`, compact storage, serialization · **Project step:** build, persist, and measure the inverted index; answer Boolean queries · **Course:** [Python — Build a Search Engine](README.md) · **Previous:** [Lab 01](lab-01-iterators-and-the-corpus.md)

---

## This lab's feature

The dictionary is Python. Every namespace, every object's attributes, every keyword argument, every module — all dictionaries. When you write `obj.name`, a dict lookup happens. The language is fast *because* its dict is fast, and the dict is fast because of forty years of accumulated cleverness that Hettinger's talk calls "a confluence of a dozen great ideas."

A search engine's core data structure — the **inverted index**, mapping each term to the list of documents containing it — is a dictionary. Building one that fits in memory for a real corpus forces you to understand what a dict actually costs, what makes an object hashable, why `dataclasses` exist, what `__slots__` buys you, and how Python objects are laid out in RAM. You'll go from "I use dicts" to "I know what a dict is," and you'll measure every claim.

---

## Theory

### 1. What a hash table is, and what Python's actually looks like

A hash table turns "find this key" from a search into an *arithmetic* operation: `hash(key)` gives an integer; that integer (masked to the table size) is the slot to look in. Average lookup is O(1) — independent of how many keys you have. That's the entire magic, and the [TimeComplexity](https://wiki.python.org/moin/TimeComplexity) page tells you the cost of every operation on every built-in.

Two keys can hash to the same slot — a **collision**. CPython resolves collisions by **open addressing**: probe another slot, using a sequence that mixes in the higher bits of the hash (`perturb`) so clustered hashes spread out. When the table is ~2/3 full it **resizes** (rebuilds at a larger size) — which is why inserting into a dict is *amortized* O(1), with occasional expensive rebuilds.

Since Python 3.6, the dict is **compact and ordered**: a small sparse *index* array of tiny integers points into a dense *entries* array of `(hash, key, value)` triples. Two consequences you'll rely on:

- Dicts preserve **insertion order** (guaranteed since 3.7). Iterate a dict and you get keys in the order they were added.
- Dicts are much smaller than they used to be — ~20–25% less memory — because the sparse part only holds 1-byte or 2-byte indices.

Sets are the same table without the values. `frozenset` is a hashable set (so it can be a key or a set member).

### 2. The hashing contract: what makes a key legal

For an object to be a dict key or a set member, it must be **hashable**: it needs `__hash__()` returning an int, and `__eq__()` so the table can confirm a match after a collision. The contract is strict:

> If `a == b`, then `hash(a) == hash(b)` must hold. **Always.**

Break this and your dict silently loses keys. This is why **mutable objects are unhashable by default**: if a list could be a key and you appended to it, its hash would change and the table would look in the wrong slot forever. `list`, `dict`, `set` — unhashable. `tuple`, `str`, `int`, `frozenset`, `bytes` — hashable. A tuple *containing* a list — unhashable (hash is recursive).

When you define a class with `__eq__` but not `__hash__`, Python sets `__hash__ = None`: your objects become unhashable. If you want them as keys you must define both, consistently, from the same fields. `@dataclass(frozen=True)` does this for you — that's the safe way to create a hashable record type.

Also: `hash("abc")` is **randomized per process** (a defense against hash-flooding attacks). Never persist raw string hashes or rely on set iteration order across runs.

### 3. `collections`: the dict's specialized relatives

- **`Counter`** — a dict subclass for counting: `Counter(tokens)`, `.most_common(50)`, `+`/`-` between counters. You used it in Lab 1; know it's *just a dict* with a `__missing__` that returns 0.
- **`defaultdict(list)`** — a dict that creates a default value on first access. `index[term].append(doc_id)` with no `if term not in index`. This is how you build postings lists cleanly. Under the hood: the `__missing__` hook, which any dict subclass can implement.
- **`deque`** — O(1) append/pop at *both* ends (a list's `pop(0)` is O(n)). Your crawler frontier in Lab 6.
- **`ChainMap`**, **`OrderedDict`** (now mostly redundant, but `move_to_end` makes an LRU cache in five lines).

The pattern to internalize: instead of `if key in d: d[key].append(x) else: d[key] = [x]`, reach for `defaultdict` or `d.setdefault(key, []).append(x)`.

### 4. `dataclasses`: records without boilerplate

A `Document` with five fields written as a class needs `__init__`, `__repr__`, `__eq__` — 15 lines of code that's easy to get subtly wrong. `@dataclass` generates them from the field declarations. Hettinger's talk calls it "the code generator to end all code generators," and it is.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Posting:
    doc_id: int
    tf: int
    positions: tuple[int, ...] = ()
```

The options that matter here:

- **`frozen=True`** — instances are immutable and therefore hashable. Records that go into sets or serve as keys should be frozen.
- **`slots=True`** (3.10+) — see the next section. Almost always what you want for records you'll have millions of.
- **`field(default_factory=list)`** — for mutable defaults. `positions: list = []` is a bug (shared between all instances); the dataclass decorator refuses to compile it. Good.
- **`order=True`** — generates `<`, `<=` etc. comparing fields in order, so `sorted(postings)` works.
- `dataclasses.asdict` / `astuple` for serialization; `replace()` for "copy with changes" on frozen instances.

Versus `NamedTuple`: a `NamedTuple` *is* a tuple (indexable, unpackable, immutable, tiny). A dataclass is a class (mutable unless frozen, can have methods that make sense, supports inheritance sanely). For a small immutable record either is fine; for anything with behavior, dataclass.

### 5. `__slots__` and where the bytes go

By default every Python object has a `__dict__` — a real dictionary holding its attributes. That's what makes `obj.new_attr = 1` work at any time. It also costs ~100+ bytes per instance *on top of* the attribute values. For a million `Posting` objects, that's 100 MB of dictionaries holding three ints each.

`__slots__ = ("doc_id", "tf")` (or `@dataclass(slots=True)`) replaces the per-instance dict with fixed C-level slots. Attribute access gets *faster* (no dict lookup) and each instance shrinks to roughly the size of its fields. The trade: you can't add attributes not declared in slots, and multiple inheritance gets fiddly.

Measure it. `sys.getsizeof(obj)` gives the *shallow* size (not what the attributes point to); for the real number, build a million of them under `tracemalloc` with and without slots. You'll see a 2–3× difference. That's the kind of number that goes in your README.

Beyond slots, when you have *millions of small integers* — postings lists — Python objects themselves are the overhead: a Python `int` is 28 bytes; a list of a million of them is ~36 MB of pointers plus objects. The [`array`](https://docs.python.org/3/library/array.html) module (`array('I', ...)`) stores them as raw 4-byte unsigned ints — **9× smaller** — and `bytes` / `memoryview` let you work with them without copying. Lab 8 pushes this into numpy; here you'll meet it as the answer to "why does my index use 3 GB?"

### 6. Sorted postings and the merge

Store each term's postings **sorted by `doc_id`**. Then Boolean queries are the classic merge algorithms from [Chapter 1 of the Stanford IR book](https://nlp.stanford.edu/IR-book/):

- **AND** — walk both lists with two pointers; emit when equal; advance the smaller. O(len(a) + len(b)), no hashing.
- **OR** — same walk, emit everything once.
- **NOT** — AND with the complement, or skip matches.

With Python sets you could do `set(a) & set(b)` — simpler, and fine for small lists. But the merge is what real engines do (it streams, it works on compressed postings, and it extends to phrase queries in Lab 3). Implement the merge; compare it to sets on your biggest terms; know when each wins.

### 7. Persistence: getting the index to disk and back

You do not want to rebuild the index on every search. Options, in order of sophistication:

- **`pickle`** — serializes almost any Python object graph in one call. Fast, easy, **and a security hole**: `pickle.load` on untrusted data executes arbitrary code. Fine for *your own* index file; never for anything received over a network. Read the [red warning box in the docs](https://docs.python.org/3/library/pickle.html) once so you never forget.
- **`json`** — safe, human-readable, interoperable, and only handles dicts/lists/strings/numbers. Tuples become lists; int keys become strings. Slower and bigger than pickle.
- **A purpose-built format** — for the postings, write `array` buffers to a binary file with a small JSON header: term → (offset, length). Then `mmap` the file and read postings without loading the whole index. This is how real engines work, and it's the Stretch for this lab.

Whatever you choose, **measure**: file size, save time, load time. Add them to the table.

### Prove it to yourself (REPL, 10 minutes)

1. `d = {}; [d.__setitem__(i, i) for i in range(10)]` — call `sys.getsizeof(d)` after 5, 6, 11, 22 inserts. Where does it jump? That's the resize.
2. Define a class with `__eq__` comparing one field but no `__hash__`. Try to put it in a set. Then add `__hash__` returning a constant `42` — it *works*; everything collides, and `in` becomes O(n). Time 10,000 lookups to see it.
3. `hash("hello")` in two separate `python -c` runs. Different? Now with `PYTHONHASHSEED=0`.
4. Build 1,000,000 instances of a 3-field class under `tracemalloc`, with and without `slots=True`. Ratio?
5. `array('I', range(10**6))` vs `list(range(10**6))` — `sys.getsizeof` both. Then explain why `getsizeof` of the list is *understating* the real cost.

---

## Project step: the inverted index

### Milestones

**M1 — Build the index in memory.**
`index.py` — a function (or class; you'll refactor to a proper class in Lab 3) that consumes the Lab 1 pipeline and produces:

- `postings: dict[str, list[Posting]]` — term → sorted-by-`doc_id` list of `Posting(doc_id, tf)` where `tf` is the term frequency in that document.
- `doc_lengths: dict[int, int]` — tokens per document (you'll need it for BM25 in Lab 3).
- `doc_meta: dict[int, DocMeta]` — `doc_id` → path/title so results can be displayed.

Use `defaultdict`, `@dataclass(frozen=True, slots=True)`, and build postings in one pass by tracking the *current* document's `Counter` and flushing it when the document ends. Keep the pipeline lazy: the corpus still streams; only the index grows.

Optionally record **positions** (`tuple[int, ...]` of token offsets) per posting. It roughly triples the index size but unlocks phrase search in Lab 3. Your call — make it a flag and measure both.

**M2 — Boolean search.**
`search.py` — parse a query of the form `term term` (implicit AND), with optional `OR` and `NOT` (a simple left-to-right evaluation is fine; Lab 3 gives it a real parser). Implement the **two-pointer merge** for AND and OR on the sorted postings lists. Return `doc_id`s; display titles via `doc_meta`.

Add a `--engine {merge,set}` flag that switches the implementation. Benchmark both on your two most common terms and your two rarest terms. Which wins where?

**M3 — Persist and reload.**
`store.py` — `save(index, path)` and `load(path) -> Index`. Start with `pickle` (and a comment explaining exactly why you'd never `load` an untrusted file). Then implement a second format of your choice — `json`, or a binary `array`-based one. Measure **file size, save time, load time** for each and put them in the table.

`python -m findex.index data/ --out index.bin` builds and saves; `python -m findex.search index.bin "query"` loads and searches. Both print elapsed time and peak memory.

**M4 — The memory study.**
Three variants of `Posting` storage, same corpus, measured under `tracemalloc`:

| Postings representation | Peak memory (build) | Index file size | Load time |
|---|---|---|---|
| `list[Posting]` with plain `@dataclass` | | | |
| `list[Posting]` with `slots=True` | | | |
| `array('I')` pairs (doc_ids, tfs) — no objects | | | |

Plus one paragraph explaining *where the bytes went* in each row. This table is the centerpiece of this lab's README section.

### Definition of done

- Index builds in one pass over a lazily streamed corpus; postings are sorted by `doc_id`.
- AND/OR/NOT queries work via a merge; a set-based alternative exists and is benchmarked.
- Save/load works in at least two formats, with size/time measured.
- The three-row memory table is in the README with real numbers and an explanation.
- `Posting` and `DocMeta` are frozen, slotted dataclasses and are hashable.
- Repo tagged `lab-02`.

---

## Deliverable checklist

- [ ] `Posting` / `DocMeta` are `@dataclass(frozen=True, slots=True)`; you can put them in a set.
- [ ] Postings built with `defaultdict` in a single streaming pass; sorted by `doc_id`.
- [ ] Two-pointer merge for AND/OR; `--engine set` alternative; benchmark of both in README.
- [ ] `save`/`load` in two formats; pickle's danger documented in a comment and the README.
- [ ] Optional positions flag, with its size cost measured if you implemented it.
- [ ] Three-row memory table with real numbers and a paragraph of explanation.
- [ ] `python -m findex.index` and `python -m findex.search` work end-to-end from a saved file.
- [ ] Git tag `lab-02`.

---

## Reflection — explain it at the whiteboard

1. Draw a hash table with 8 slots. Insert three keys where two collide. Show how CPython finds the second one on lookup.
2. State the hashing contract. Give a class that violates it and show, concretely, how a dict "loses" a key.
3. Why are lists unhashable but tuples hashable? Why is `(1, [2])` unhashable?
4. What does `@dataclass(frozen=True)` change about `__hash__`? What happens to `__hash__` if you define `__eq__` by hand and forget it?
5. Where do the ~100 bytes per plain instance go, and how does `__slots__` eliminate them? What do you give up?
6. Your `array('I')` row is N× smaller than the `list[Posting]` row. Account for the N: what is each element's size in each representation?
7. Two-pointer merge vs `set(a) & set(b)`: complexity of each, and when did each win in your benchmark? Why?
8. Why is `pickle.load` on a downloaded file a remote-code-execution vulnerability?

---

## Stretch

Build the **binary, `mmap`-able index format**: one file with a JSON header (term → byte offset, count) and the postings as contiguous `array('I')` buffers. Load via `mmap` so that searching touches only the postings you need and *load time is constant regardless of index size*. Measure load time vs. pickle at 10×, 100× corpus size. Then implement **gap encoding** (store `doc_id` deltas instead of absolute ids) and note how much smaller the file gets — you've just reinvented the first step of real index compression.

---

## Resources

**Watch**

- Raymond Hettinger — [Modern Python Dictionaries: A Confluence of a Dozen Great Ideas (PyCon 2017, 45 min)](https://www.youtube.com/watch?v=npw4s1QTmPg). The definitive history and design of the compact ordered dict, told by the person who designed much of it. This is Section 1 in full.
- Brandon Rhodes — [The Dictionary Even Mightier (PyCon 2017, 45 min)](https://www.youtube.com/watch?v=66P5FMkWoVU). Same subject, complementary angle: hash tables from first principles, collision resolution, and how each feature was motivated by a trade-off. Rhodes is one of the best explainers in the Python world.
- Raymond Hettinger — [Dataclasses: The Code Generator to End All Code Generators (PyCon 2018, 50 min)](https://www.youtube.com/watch?v=T-TwcmT6Rcw). What dataclasses generate, why, and how they compare to namedtuples and attrs. Section 4.

**Read**

- Python docs — [Time Complexity of built-in operations](https://wiki.python.org/moin/TimeComplexity). One page; memorize the table.
- Python docs — [`collections`](https://docs.python.org/3/library/collections.html), [`dataclasses`](https://docs.python.org/3/library/dataclasses.html), [`array`](https://docs.python.org/3/library/array.html), [`pickle`](https://docs.python.org/3/library/pickle.html) (read the security warning). The reference docs are excellent here.
- Real Python — [Data Classes in Python](https://realpython.com/python-data-classes/). Thorough walkthrough of every option, including `slots` and `frozen` with memory measurements.
- Python docs — [Sorting HOWTO](https://docs.python.org/3/howto/sorting.html). `key=`, stability, `operator.itemgetter`/`attrgetter` — you'll sort postings and results constantly.
- Manning, Raghavan & Schütze — [*Introduction to Information Retrieval*](https://nlp.stanford.edu/IR-book/), Chapter 1 ("Boolean retrieval") and Chapter 4 ("Index construction"). The free Stanford textbook this whole project is implicitly following. Chapter 1 is the inverted index and the merge algorithm; twenty pages.
- *Fluent Python*, 2nd ed. — Chapter 3 ("Dictionaries and Sets") and Chapter 5 ("Data Class Builders").
