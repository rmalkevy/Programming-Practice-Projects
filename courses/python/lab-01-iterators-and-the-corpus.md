# Lab 01 — Streams, Not Lists: Iterators, Generators, and Your Corpus

> "Loop like a native."
> — Ned Batchelder

**Weeks:** 1–2 · **Language focus:** the iteration protocol, generators, lazy pipelines, `pathlib`, `re`, Unicode text · **Project step:** choose a corpus and stream it into tokens and term statistics in constant memory · **Course:** [Python — Build a Search Engine](README.md)

---

## This lab's feature

Most programmers coming from C++, Java, or JavaScript write Python like this: read everything into a list, then loop over the list, then build another list. It works — until the corpus is 2 GB and the list is 6 GB and the laptop stops responding.

Python's deepest idiom is **iteration**. The `for` loop isn't a counter; it's a protocol that any object can speak. Generators let you write functions that produce values *one at a time, on demand*, holding only the current item in memory. Chain a few of them and you have a **lazy pipeline**: a corpus of any size flows through tokenization and counting using the same few kilobytes of RAM.

This is the idiom that separates people who "know Python" from people who write Python. It's also where the language's most famous features — comprehensions, `itertools`, `yield`, file iteration, even `asyncio` (Lab 6) — come from. You'll learn it by building the intake of your search engine: **a corpus loader and tokenizer that never load the corpus into memory**.

---

## Theory

### 1. The iteration protocol: what `for` actually does

When you write `for x in thing:`, Python doesn't index `thing` with `0, 1, 2, …`. It does this:

```python
it = iter(thing)          # calls thing.__iter__()  -> returns an *iterator*
while True:
    try:
        x = next(it)      # calls it.__next__()     -> returns the next value
    except StopIteration: # the iterator signals "I'm done" by raising
        break
    ...body...
```

Two distinct roles:

- An **iterable** is anything with `__iter__()` that returns an iterator. Lists, strings, dicts, files, ranges, your own classes.
- An **iterator** is an object with `__next__()` (and `__iter__()` returning itself). It has *state*: it knows where it is. Call `next()` and it advances. When exhausted, it raises `StopIteration` — forever.

This is why a list can be looped over twice but an iterator can't: the list hands out a *fresh* iterator each time; the iterator *is* the position. And it's why `len()` doesn't work on an iterator — it doesn't know how many items remain until it produces them.

Write an iterator by hand once in your life, so you never forget it:

```python
class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for i in Countdown(3):
    print(i)          # 3, 2, 1
```

### 2. Generators: iterators without the boilerplate

Any function containing `yield` becomes a **generator function**. Calling it runs *nothing* — it returns a generator object, which is an iterator. Each `next()` runs the body until the next `yield`, hands out that value, and **freezes the function's entire state** (locals, position) until the next `next()`.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

g = countdown(3)      # nothing has run yet
next(g)               # 3  -- runs to the first yield, pauses
next(g)               # 2
next(g)               # 1
next(g)               # StopIteration
```

That 4-line function is the `Countdown` class above, minus the class. A generator is a *resumable function*. The key consequences:

- **Lazy.** Work happens only when someone asks for the next value. `countdown(10**12)` returns instantly.
- **Constant memory.** Only the current value exists. There is no list.
- **Single-pass.** Once exhausted, it's done. To iterate again, call the function again.
- **Composable.** A generator can consume another generator. That's a pipeline.

A **generator expression** is the inline form: `(x * x for x in range(10))`. Same laziness, no function needed. Compare to the list comprehension `[x * x for x in range(10)]`, which builds the whole list immediately. Rule of thumb: **square brackets when you need the list; parentheses when you just need to loop over it once.**

`yield from other_iterable` delegates to another iterable — it's how you flatten one generator into another cleanly:

```python
def all_lines(paths):
    for path in paths:
        with open(path, encoding="utf-8") as f:
            yield from f          # yield each line of this file, then move on
```

### 3. Pipelines: the Unix philosophy inside one process

The real power appears when you chain generators. Each stage pulls from the one before it, one item at a time. Nothing is materialized:

```python
def read_docs(root):            # Path -> yields (path, text)
    ...
def tokenize(text):             # str  -> yields tokens
    ...

docs   = read_docs(Path("corpus"))
tokens = (tok for _, text in docs for tok in tokenize(text))
counts = Counter(tokens)        # the only thing that grows: the term table
```

A 10 GB corpus flows through this with memory usage equal to *one document plus the counter*. The `Counter` is the sink — the one data structure that legitimately grows, because it holds the *answer*. Everything upstream is a stream.

The standard library ships a toolbox for this in [`itertools`](https://docs.python.org/3/library/itertools.html) — learn these five: `islice` (take the first N of a stream — indispensable for testing on a slice of the corpus), `chain` (concatenate streams), `groupby` (group *consecutive* equal items), `takewhile` / `dropwhile`, and `batched` (3.12+, chunk a stream into tuples of N). Also `map` and `filter` are lazy in Python 3, and `enumerate` and `zip` are too.

### 4. Files are iterators (and how to read text correctly)

An open text file is an iterator over its lines — lazily. `for line in f:` reads one line at a time, however big the file. `f.read()` reads all of it into one string; `f.readlines()` builds a list of all lines. For a search engine, the first is the right default and the other two are the bug you'll regret.

Use [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html), not string paths: `Path("corpus").rglob("*.txt")` is a lazy generator over every matching file in the tree, and `path.read_text(encoding="utf-8")` / `path.open(encoding="utf-8")` are explicit about encoding.

**Always pass `encoding=`.** Python's default text encoding depends on the OS and locale (Windows is the usual culprit). Your corpus is almost certainly UTF-8; say so. For messy real-world corpora, `errors="replace"` (turn undecodable bytes into `�`) or `errors="ignore"` keeps one bad file from crashing a ten-hour index build — but log it.

### 5. Text is harder than it looks: Unicode and tokenization

A **token** is the unit your index will store — usually a word. Turning text into tokens is called tokenization, and doing it *well* on real text is where search engines quietly win or lose.

- **Use `re.finditer`, not `re.findall`.** `findall` builds a list of every match; `finditer` yields match objects lazily. Same regex, streaming result.
- **`\w` is Unicode-aware in Python 3.** `r"\w+"` matches Cyrillic, accented Latin, CJK — not just ASCII. Good: your Ukrainian notes tokenize correctly. Watch for apostrophes in words (`don't`, `п'ять`) — decide a policy.
- **Case: use `str.casefold()`, not `lower()`.** `casefold` is the aggressive, locale-independent normalization designed for caseless matching (`"ß".casefold() == "ss"`, `"Straße"` matches `"STRASSE"`). `lower()` misses these.
- **Normalize Unicode with `unicodedata.normalize("NFC", text)`.** The same visible character can be encoded as one code point or as a base + combining mark (`é` as `U+00E9` or as `e` + `U+0301`). If you don't normalize, `"café"` and `"café"` become different tokens and half your results vanish. NFC is the standard choice for text you'll compare.
- Store the **document offsets** of tokens if you want phrase search later (Lab 3). `match.start()` gives you that for free.

Read [the Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) once; it's the fastest way to stop being scared of `UnicodeDecodeError`.

### 6. Measuring, not guessing

"It uses less memory" is a claim; a number is evidence. Two tools:

- [`tracemalloc`](https://docs.python.org/3/library/tracemalloc.html) — `tracemalloc.start()`, run the code, `tracemalloc.get_traced_memory()` returns `(current, peak)` in bytes. Peak is what you report.
- `time.perf_counter()` for wall-clock timing of a block (Lab 3 will wrap this in a decorator).

You will produce a table this lab: eager vs. lazy, peak memory and elapsed time, on the same corpus. That table goes in your README.

### 7. Pitfalls that bite everyone once

- **Exhausted generator, silently empty.** You iterate a generator to count it, then iterate it again to process it — the second loop does nothing. Generators are single-pass; if you need two passes, you need two generators (call the function twice) or a list.
- **`len(gen)` / `gen[0]`.** Iterators have no length and no indexing. Use `itertools.islice` for "the first N" and count with `sum(1 for _ in gen)` if you must (that consumes it).
- **Laziness moves errors.** A bug inside a generator doesn't raise when you *create* it, only when you *consume* it — often far away in the code. Read tracebacks accordingly.
- **Accidental materialization.** `sorted(gen)`, `list(gen)`, `", ".join(gen)`, `set(gen)` all pull the whole stream into memory. Sometimes you want that; know when you're doing it.
- **Holding a reference kills the benefit.** `lines = list(f)` then `for line in lines` — you built the list; laziness is gone. Pass generators along, don't store them.

### Prove it to yourself (REPL, 10 minutes)

1. `it = iter([1, 2, 3])`; call `next(it)` four times. Then `for x in it: print(x)` — why does nothing print?
2. Compare peak memory: `sum([x * x for x in range(10**7)])` vs `sum(x * x for x in range(10**7))` under `tracemalloc`. Explain the ratio.
3. `g = (print(i) or i for i in range(3))` — nothing prints. `next(g)` — now something prints. What does this tell you about when generator bodies run?
4. `"café" == unicodedata.normalize("NFC", "cafe\u0301")` — evaluate both sides with and without normalization.
5. `open` a file, iterate it once with `for`, then try again. What happens, and how does this relate to Pitfall 1?

---

## Project step: the corpus intake

### Choose your corpus

Pick something you'll enjoy searching, with **at least ~1,000 documents or ~50 MB of text** by the end of the course. Start with a small slice so iteration takes seconds; scale up once the code is right. Good options:

- **Your own notes** — lecture notes, an Obsidian vault, exported chats. The most satisfying to search.
- **[Project Gutenberg](https://www.gutenberg.org/ebooks/search/?sort_order=downloads)** — thousands of public-domain books as plain `.txt`. One document per book, or split by chapter.
- **Wikipedia** — the [Simple English dump](https://dumps.wikimedia.org/simplewiki/latest/) is a manageable ~300 MB; the [`wikimedia/wikipedia` dataset on Hugging Face](https://huggingface.co/datasets/wikimedia/wikipedia) has per-language parquet files (including Ukrainian) that are easy to load.
- **[arXiv abstracts](https://www.kaggle.com/datasets/Cornell-University/arxiv)** — 2 M+ scientific abstracts as one big JSON-lines file. Great for streaming: one line = one document.
- **[20 Newsgroups](https://scikit-learn.org/stable/datasets/real_world.html)** — the classic small text-classification corpus; ~18,000 posts.
- **The Python docs**, a framework's docs, or any site you'll crawl yourself in Lab 6.

Whatever you pick, get it into a directory of plain-text files (or one JSON-lines file) under `data/` — and **add `data/` to `.gitignore`**. Corpora don't go in git.

### Set up the project

```bash
uv init findex --lib          # creates pyproject.toml and a src/findex/ layout
cd findex
uv add --dev ruff pytest
git init && git add . && git commit -m "Lab 1: project skeleton"
```

Target layout at the end of this lab:

```txt
findex/
  pyproject.toml
  README.md
  .gitignore                 # includes data/
  data/                      # your corpus (not committed)
  src/findex/
    __init__.py
    corpus.py                # iter_documents(root) -> Iterator[Document]
    tokenize.py              # tokenize(text) -> Iterator[str]
    stats.py                 # the pipeline + `python -m findex.stats`
  tests/
    test_tokenize.py         # a few asserts now; real pytest in Lab 4
```

### Milestones

**M1 — Lazy document stream.**
`corpus.py` exposes `iter_documents(root: Path) -> Iterator[Document]`, where `Document` is a `NamedTuple` (or `dataclass`) of `doc_id`, `path`, `text`. It must be a generator: opening one file at a time, yielding it, moving on. Support at least one of: a directory tree of `.txt` files (`rglob`), or a JSON-lines file (one document per line). Handle bad encodings without crashing (log and continue).

*Check:* `next(iter_documents(Path("data")))` returns instantly, even on a 500 MB corpus.

**M2 — Streaming tokenizer.**
`tokenize.py` exposes `tokenize(text: str) -> Iterator[str]`: NFC-normalize, `casefold`, then `re.finditer` over a word pattern you've chosen and documented. Decide and document your policy for apostrophes, hyphens, and digits. Write 6–10 `assert`-style checks in `tests/test_tokenize.py` covering: mixed case, Cyrillic text, a combining-mark accent, punctuation, an empty string.

**M3 — The stats pipeline.**
`stats.py` chains the two into a pipeline and computes, in a single pass: number of documents, total tokens, vocabulary size, and the **top-50 terms** with counts. `python -m findex.stats data/` prints the results plus **elapsed time and peak memory** (`tracemalloc`). Support a `--limit N` flag (via `itertools.islice`) so you can run on the first N documents while developing.

*Check:* run it on your full corpus. Peak memory should be roughly *one document + the Counter*, not the corpus size.

**M4 — The measurement.**
Write the *eager* version deliberately (read all documents into a list, tokenize into a list of lists, then count). Run both on the same corpus slice (as large as the eager one survives). Put a table in your README:

| Version | Documents | Peak memory | Elapsed |
|---|---|---|---|
| eager (lists) | … | … | … |
| lazy (generators) | … | … | … |

Then one paragraph, in your own words, explaining *why* the numbers differ and where in the pipeline the memory went.

### Definition of done

- `iter_documents` and `tokenize` are generators, and you can demonstrate it (`inspect.isgeneratorfunction`, or just show `next()` returning before the corpus is read).
- The stats command runs on your full corpus without loading it into memory.
- The eager-vs-lazy table is in the README with real numbers from your machine.
- Tokenizer choices are documented and tested.
- Repo is tagged `lab-01`.

---

## Deliverable checklist

- [ ] Public repo, `src/` layout, `uv`-managed, `ruff` clean.
- [ ] `data/` in `.gitignore`; README says where the corpus comes from and how to get it.
- [ ] `iter_documents` and `tokenize` are generators; `--limit` uses `islice`.
- [ ] Tokenizer applies NFC + `casefold`; policy for apostrophes/hyphens/digits is written down.
- [ ] `tests/test_tokenize.py` with 6–10 checks, including Cyrillic and a combining-mark case.
- [ ] `python -m findex.stats data/` prints doc count, token count, vocabulary size, top-50 terms, elapsed, peak memory.
- [ ] README has the eager-vs-lazy table with real numbers and a one-paragraph explanation.
- [ ] Git tag `lab-01`.

---

## Reflection — explain it at the whiteboard

1. Desugar `for x in xs:` into `iter` / `next` / `StopIteration` on the board. What's the difference between an iterable and an iterator, and which one is a generator object?
2. Why can a list be looped over twice but a generator can't? What would you have to do to a generator to make it "restartable"?
3. Your pipeline is `Counter(tok for doc in docs for tok in tokenize(doc.text))`. Walk through what's in memory at the moment the 10,000th token is being counted.
4. Where does an exception raised *inside* `tokenize` actually surface, and why is that far from the `def`?
5. Why `casefold()` and not `lower()`? Why NFC? Give one concrete input where each makes the difference.
6. `re.findall` vs `re.finditer` — same regex, what's the memory difference on a 100 MB document?
7. Show your eager-vs-lazy table. Where did the eager version's memory go, exactly? Why isn't the lazy version's memory *zero*?

---

## Stretch

Make `iter_documents` handle **compressed corpora without extracting them** — `gzip.open` / `bz2.open` / a `zipfile` — and streaming JSON-lines from a `.jsonl.gz`. Then benchmark tokenizing with `re.finditer` against `str.split()` + manual cleanup, and against splitting on the [`regex`](https://pypi.org/project/regex/) module's `\p{L}+` (Unicode letter class). Which is fastest? Which is *right*? Put the answer in your README.

---

## Resources

**Watch**

- Ned Batchelder — [Loop Like a Native (PyCon 2013, 30 min)](https://www.youtube.com/watch?v=EnSu9hHGq5o). *The* talk on Python iteration: why you never write `for i in range(len(x))`, and how to think in iterables. Watch this first.
- Corey Schafer — [Python Generators (11 min)](https://www.youtube.com/watch?v=bD05uGo_sVI). Short, concrete, with a memory comparison you can reproduce. Good as a quick second pass.
- James Powell — [So you want to be a Python expert? (PyData 2017, 1h40)](https://www.youtube.com/watch?v=cKPlPJyQrt4). A live-coded tour of the data model, generators, decorators, and context managers — essentially the theory of Labs 1–3 in one sitting. Watch the generators section now; you'll come back for the rest.

**Read**

- Trey Hunner — [The Iterator Protocol: How `for` Loops Work in Python](https://treyhunner.com/2016/12/python-iterator-protocol-how-for-loops-work/). The cleanest written explanation of Section 1; ten minutes.
- Real Python — [How to Use Generators and `yield` in Python](https://realpython.com/introduction-to-python-generators/). Thorough, with a large-CSV example that mirrors this lab exactly.
- Python docs — [Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html) (iterators, generators, `itertools` — read the first half) and the [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html) (the encoding half of this lab).
- David Beazley — *Generator Tricks for Systems Programmers*, via his [tutorials page](http://dabeaz.com/tutorials.html). The 2008 classic that taught a generation of Python programmers to build pipelines out of generators. Its log-file examples are your corpus pipeline with different nouns.
- Joel Spolsky — [The Absolute Minimum Every Software Developer Must Know About Unicode](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/). Twenty years old and still the best 15-minute fix for "what even is an encoding."
- *Fluent Python*, 2nd ed. — Chapter 17, "Iterators, Generators, and Classic Coroutines." If you own one Python book, it's [this one](https://www.fluentpython.com/).
