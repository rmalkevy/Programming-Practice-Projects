# Lab 04 — Make It a Real Tool: Typing, Testing, Packaging, and a CLI

> "Untested code is broken code you haven't noticed yet. Unpackaged code is a script only you can run."

**Weeks:** 7–8 · **Language focus:** type hints and static checking, `pytest` and property-based testing, `pyproject.toml` and `uv`, entry points, `typer` + `rich`, `logging`, CI · **Project step:** `findex` becomes an installable, typed, tested command-line tool with CI · **Course:** [Python — Build a Search Engine](README.md) · **Previous:** [Lab 03](lab-03-the-object-model-and-ranking.md)

---

## This lab's feature

Everything so far runs with `python -m findex.something` from inside your repo, has no type annotations you're actually checking, and has a folder of `assert` statements for tests. That's a research prototype. This lab turns it into **software**: the thing a colleague installs with one command, that a type checker has verified, that a test suite proves correct on every push.

Modern Python has quietly become a typed language with a real toolchain. Type hints plus `pyright`/`mypy` catch entire classes of bugs before you run anything, and they make FastAPI (Lab 7) work at all. `pytest` is the most pleasant test framework in any language. `uv` has made packaging — Python's historical embarrassment — fast and boring. Knowing this stack fluently is the difference between "writes Python scripts" and "ships Python software," and it's what every code review at a real company will assume.

---

## Theory

### 1. Gradual typing: what type hints are, and aren't

Python's type hints (PEP 484 and successors) are **annotations the interpreter ignores** at runtime. `def df(self, term: str) -> int:` runs identically to the unannotated version. Their consumers are *tools*: type checkers, IDEs (autocomplete, refactoring), and libraries that read annotations at import time (dataclasses, FastAPI, Pydantic, typer).

Typing is **gradual**: you can annotate one function or the whole codebase; unannotated code is `Any`, which the checker doesn't check. The goal in this lab is a codebase where **pyright in strict mode passes** — no `Any` leaking through your public API.

The vocabulary you need (modern syntax, 3.12+):

- Built-in generics: `list[str]`, `dict[str, list[Posting]]`, `tuple[int, ...]`, `set[int]`. Not `List`/`Dict` from `typing` — those are legacy.
- `X | None` instead of `Optional[X]`. The checker forces you to handle the `None` branch — **narrowing**: after `if x is None: return`, `x` is known to be `X`.
- `Iterator[str]` / `Iterable[str]` (from `collections.abc`) as the return type of a generator function — `Iterator` if the caller may `next()` it, `Iterable` if they'll just loop. Accept `Iterable`, return `Iterator`: be liberal in what you accept, precise in what you return.
- `typing.Protocol` — structural interfaces. Your `Scorer` from Lab 3 becomes a `Protocol` and pyright verifies both implementations satisfy it *without* inheritance.
- Generics with the PEP 695 syntax: `def first[T](xs: Iterable[T]) -> T:` and `class ResultList[T]:`. No more `TypeVar` boilerplate.
- `Literal["merge", "set"]` for enum-like string parameters; `TypedDict` for JSON-shaped dicts; `Final` for constants; `@overload` when return type depends on argument type; `TypeAlias`/`type DocId = int` for readability.
- `typing.cast` and `# type: ignore[code]` are the escape hatches. Every one is a small debt; comment why.

**pyright vs mypy:** both work; pyright is faster, stricter by default, and is what VS Code's Pylance uses. Pick one (pyright recommended), configure it in `pyproject.toml`, and run it in CI.

### 2. `pytest`: the test framework that gets out of your way

Plain functions named `test_*`, plain `assert`, rich failure output. That's 80% of pytest. The other 20% is what makes it excellent:

- **Fixtures** — `def index(tmp_path): ...` provides a built index to any test that lists `index` as a parameter. Scope them (`scope="session"`) so an expensive corpus is built once per run. Built-ins you'll use: `tmp_path` (a fresh temp directory), `monkeypatch` (patch env vars/attributes and auto-restore), `capsys` (capture stdout), `caplog` (capture logs).
- **`@pytest.mark.parametrize`** — one test, many inputs, each reported separately. Your tokenizer tests from Lab 1 become a parametrized table.
- **`pytest.raises`** — assert that an exception is raised, and inspect it.
- **Markers** — `@pytest.mark.slow`; run `-m "not slow"` during development, everything in CI.
- **`conftest.py`** — shared fixtures for a directory tree; a small corpus fixture belongs here.
- **Coverage** — `pytest --cov=findex`; aim for the *important* paths, not a number. 100% coverage with no assertions is worse than 70% with sharp ones.

Design for testability: the thing Brandon Rhodes calls **"hoist your I/O"** — keep pure logic (tokenize, score, merge, parse) separate from I/O (files, network, printing), so the logic is trivially testable with in-memory data and the I/O is thin. Your Lab 1–3 code is mostly already shaped this way; where it isn't, refactor.

### 3. Property-based testing: let the computer invent the test cases

Example-based tests check the cases *you* thought of. [Hypothesis](https://hypothesis.readthedocs.io/) generates hundreds of inputs from a strategy and checks a **property** — then, when it finds a failure, **shrinks** it to the smallest failing example. Properties you can state about `findex`:

- **Round-trip:** `load(save(index)) == index` for any index.
- **Idempotence:** `tokenize(" ".join(tokenize(text))) == tokenize(text)`.
- **Invariants:** postings are always sorted; `merge_and(a, b) == sorted(set(a) & set(b))` for any two sorted lists; query parser output re-renders and re-parses to an equal tree.
- **Oracle:** the fast implementation agrees with the obviously-correct slow one — your merge vs. Python sets.

Hypothesis finds the Unicode edge cases, the empty inputs, and the off-by-ones you'd never write down. Hillel Wayne's talk is the best introduction to this way of thinking.

### 4. Packaging: `pyproject.toml`, `uv`, and entry points

A modern Python project is described by **one file**, `pyproject.toml` (PEP 621): name, version, dependencies, optional dependency groups, and tool configuration (`[tool.ruff]`, `[tool.pytest.ini_options]`, `[tool.pyright]`). No `setup.py`, no `requirements.txt`.

[`uv`](https://docs.astral.sh/uv/guides/projects/) manages the whole lifecycle: `uv add httpx` adds a dependency and updates `uv.lock` (exact, reproducible versions — **commit it**); `uv run pytest` runs in the project's environment without activating anything; `uv sync` recreates the environment from the lockfile on another machine; `uv build` produces a wheel; `uvx` runs a tool in an isolated environment.

Two packaging concepts that matter:

- **The `src/` layout** — your code in `src/findex/`, tests outside it. It guarantees your tests run against the *installed* package, not the working directory by accident. The [Packaging Guide explains the trade-offs](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/); use `src/`.
- **Entry points** — `[project.scripts] findex = "findex.cli:app"` in `pyproject.toml` makes a `findex` command appear on the user's `PATH` after `uv tool install .` (or `pip install .`). That's how `ruff`, `pytest`, and `uv` itself get their commands.

**Versioning:** use [semantic versioning](https://semver.org/) from day one — `0.4.0` for this lab. Tags in git; `uv build` embeds it.

### 5. A CLI people want to use: `typer` + `rich`

[`typer`](https://typer.tiangolo.com/) builds a CLI from type-annotated functions — the same idea as FastAPI (same author). `def search(query: str, k: int = 10, scorer: Scorer = Scorer.bm25)` becomes `findex search "query" --k 10 --scorer bm25` with `--help`, validation, and shell completion generated for you. Subcommands are functions on the same `app`. Your type hints from Section 1 are doing double duty.

[`rich`](https://rich.readthedocs.io/) does the output: tables for results, `[bold]` highlighted snippets, a progress bar for indexing, pretty tracebacks. A search tool that prints a beautiful ranked table is more convincing than one that prints tuples.

Rules: **exit codes** (0 success, nonzero on failure — `raise typer.Exit(code=1)`); **stderr for diagnostics, stdout for data** so `findex search q | jq` works when you add `--json`; and never let a traceback reach a user for an expected error (missing index file, bad query syntax) — catch it, print one clear line, exit nonzero.

### 6. `logging`, not `print`

`print` is for CLI *output*. Everything else — timings, warnings about undecodable files, cache hits — is **logging**: leveled (`DEBUG`/`INFO`/`WARNING`/`ERROR`), switchable at runtime (`-v` → `INFO`, `-vv` → `DEBUG`), routable (stderr, a file, JSON for a log aggregator). Pattern: `log = logging.getLogger(__name__)` at the top of every module; configure *once* in the CLI entry point (never in library code). Use `log.info("indexed %d docs", n)` — lazy `%` formatting, not f-strings, so the string is built only if the level is enabled. The [Logging HOWTO](https://docs.python.org/3/howto/logging.html) covers everything you need in twenty minutes. Your `@timed` decorator from Lab 3 should log at `DEBUG`.

### 7. CI: the tests run whether you remember or not

A GitHub Actions workflow (`.github/workflows/ci.yml`) that on every push runs: `uv sync`, `ruff check`, `ruff format --check`, `pyright`, `pytest`. Twenty lines; the [quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart) plus uv's own [GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/) get you there. A green badge in the README is table stakes for a portfolio project; more importantly, it's the habit.

### Prove it to yourself (REPL/terminal, 10 minutes)

1. Annotate a function wrong on purpose (`-> int` but return a `str`). Run it — it works. Run `pyright` — it doesn't. That's the whole idea.
2. `def f(x: str | None): return x.upper()` — pyright's exact complaint? Add the `if x is None` guard; watch it disappear. That's narrowing.
3. Write a pytest test that fails. Read the assertion diff pytest prints for `assert {"a": 1} == {"a": 2}`. Compare to a bare `assert`.
4. `from hypothesis import given, strategies as st` — `@given(st.text())` a test that `tokenize` never yields an empty string. Does it find a case you didn't expect?
5. `uv build`; look inside `dist/*.whl` (it's a zip). `uvx --from dist/findex-*.whl findex --help` — your tool, running from a wheel, in an isolated environment.

---

## Project step: `findex` becomes a tool

### Milestones

**M1 — Fully typed, pyright strict.**
Annotate every public function and method in `src/findex`. Convert `Scorer` to a `typing.Protocol`. Use `Iterator`/`Iterable` correctly on the generator pipeline, `Literal` for engine/scorer names, PEP 695 generics where a generic helps. Configure `[tool.pyright] typeCheckingMode = "strict"` and get to zero errors. Every `# type: ignore` needs a reason in a comment.

**M2 — A real test suite.**
Move to `pytest`. Target **≥ 30 tests** covering: tokenizer (parametrized, including Unicode), index build on a tiny fixture corpus (`conftest.py`), the merge algorithms, the query parser (tree equality), both scorers (the three sanity checks from Lab 3 as tests), save/load round trip, and the CLI via `typer.testing.CliRunner`. Add **≥ 3 Hypothesis properties** from Section 3. Mark anything over a second `slow`. Run with coverage and put the number (and what's *not* covered, and why) in the README.

**M3 — Packaged CLI.**
`pyproject.toml` with metadata, dependencies, optional `dev` group, tool configs, and `[project.scripts] findex = "findex.cli:app"`. A `typer` app with subcommands:

- `findex index <corpus> --out <file> [--positions] [--limit N]` — with a `rich` progress bar.
- `findex search <index> "<query>" [--k 10] [--scorer bm25|tfidf] [--json]` — a `rich` table of ranked results with highlighted snippets; `--json` emits JSON lines to stdout for piping.
- `findex stats <index>` — the Lab 1 numbers, prettily.
- `-v / -vv` on the root command sets the logging level; all diagnostics go to stderr.

`uv tool install .` puts `findex` on your PATH. `uv build` produces a wheel; the README shows installing from it.

**M4 — Logging + CI + release.**
Replace every diagnostic `print` with `logging`. Add `.github/workflows/ci.yml` running ruff, pyright, pytest on push and PR; add the badge to the README. Tag `v0.4.0`, attach the wheel to a **GitHub Release**. From a clean machine (or a fresh container): `uv tool install <wheel-url>` → `findex --help` works. That's the definition of "shipped."

### Definition of done

- `pyright` strict passes; `ruff check` and `ruff format --check` pass.
- ≥ 30 pytest tests including ≥ 3 Hypothesis properties; CLI tested with `CliRunner`; coverage reported.
- `findex` installs as a command via `uv tool install`; three subcommands work; `--json` mode pipes cleanly.
- Diagnostics go through `logging` to stderr with `-v/-vv`; expected errors exit nonzero with one clear line.
- CI green on GitHub; wheel attached to a `v0.4.0` release.
- Repo tagged `lab-04`.

---

## Deliverable checklist

- [ ] `pyproject.toml` (PEP 621) with deps, `dev` group, `[project.scripts]`, and tool config; `uv.lock` committed.
- [ ] `pyright` strict: 0 errors; every `# type: ignore` justified.
- [ ] `Scorer` is a `typing.Protocol`; generators typed with `Iterator`/`Iterable`.
- [ ] ≥ 30 tests, ≥ 3 Hypothesis properties, `conftest.py` fixture corpus, `slow` marker, coverage number in README.
- [ ] `findex index|search|stats` via typer with rich output; `--json`; `-v/-vv`; nonzero exits on expected errors.
- [ ] `logging` throughout; configured once in `cli.py`; stderr for diagnostics.
- [ ] CI workflow green; badge in README; wheel on a `v0.4.0` GitHub Release; install-from-release verified.
- [ ] Git tag `lab-04`.

---

## Reflection — explain it at the whiteboard

1. Type hints are ignored at runtime. So what exactly is checking them, and when? Name three different consumers of annotations.
2. What is narrowing? Show a `str | None` example where pyright complains and how the guard fixes it.
3. `Iterator` vs `Iterable` — which do you *accept*, which do you *return*, and why?
4. What is a Protocol, and how does pyright decide your `BM25` class satisfies `Scorer` without any inheritance?
5. Explain fixture scope. What goes wrong if your session-scoped index fixture is mutated by one test?
6. State a property (not an example) about your merge function. How does Hypothesis's shrinking help when it fails?
7. Why the `src/` layout? What bug does it prevent that a flat layout allows?
8. What does `[project.scripts]` actually create on disk when you install the wheel?
9. Why `log.info("n=%d", n)` rather than `log.info(f"n={n}")`?

---

## Stretch

Add **shell completion** (`findex --install-completion`) and a **`findex config`** subcommand backed by a `TypedDict`/Pydantic settings file in the user's config directory (`platformdirs`). Then make the test suite run under **both** the GIL and free-threaded Python 3.13 in a CI matrix — you'll want that in place for Lab 5. Finally, publish to **TestPyPI** with `uv publish` so `uvx --index testpypi findex` works for anyone.

---

## Resources

**Watch**

- Carl Meyer — [Type-checked Python in the Real World (PyCon 2018, 30 min)](https://www.youtube.com/watch?v=pMgmKJyWKn8). From Instagram's migration of a multi-million-line codebase: what gradual typing buys, how to adopt it incrementally, and the gotchas. Section 1 with battle scars.
- Hillel Wayne — [Beyond Unit Tests: Taking Your Testing to the Next Level (PyCon 2018, 30 min)](https://www.youtube.com/watch?v=MYucYon2-lk). Property-based testing with Hypothesis, and *how to think of properties*. Will change how you test.
- Brandon Rhodes — [Hoist Your I/O (PyWaw Summit 2015, 45 min)](https://www.youtube.com/watch?v=PBQN62oUnN8). Why separating pure logic from I/O makes code testable, with a refactoring done live. Read before M2.

**Read**

- mypy docs — [Type hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html). One page; the syntax for everything. (Applies to pyright too.)
- [pyright docs](https://microsoft.github.io/pyright/) — configuration and the strict-mode rule list. Also the [`typing` module reference](https://docs.python.org/3/library/typing.html) and [PEP 695](https://peps.python.org/pep-0695/) for the new generics syntax.
- pytest docs — [How to use fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html). The one concept in pytest worth reading the docs for.
- [Hypothesis documentation](https://hypothesis.readthedocs.io/) — quick start, then "What you can generate and how."
- Hynek Schlawack — [Testing & Packaging](https://hynek.me/articles/testing-packaging/). The essay that made the `src/` layout standard, and why. Short and sharp.
- Python Packaging Authority — [Packaging User Guide](https://packaging.python.org/) — specifically "Writing your pyproject.toml." And [uv — Working on projects](https://docs.astral.sh/uv/guides/projects/), the uv guide you'll follow.
- [typer docs](https://typer.tiangolo.com/) (tutorial, then "Testing") and [rich docs](https://rich.readthedocs.io/) (tables, progress, console markup).
- Python docs — [Logging HOWTO](https://docs.python.org/3/howto/logging.html). Read the basic and advanced tutorials; skip the cookbook until you need it.
- GitHub — [Actions quickstart](https://docs.github.com/en/actions/writing-workflows/quickstart) and [uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/).
