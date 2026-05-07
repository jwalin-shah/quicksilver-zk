# tensor-quicksilver-zk Dependency Surface Audit

Queue item: `tensor-quicksilver-zk-dependency-surface`  
Repo path: `/Users/jwalinshah/projects/agent-stack/.agent-stack-worktrees/2026-05-07-overnight-marathon/tensor-quicksilver-zk-dependency-surface`  
Source repo: `tensor-quicksilver-zk` / `/Users/jwalinshah/projects/tensor/quicksilver-zk`  
Branch audited: `codex/goal-tensor-quicksilver-zk-dependency-surface`  
HEAD at audit start: `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`  
Focus area: `dependency-surface`

## Executive Summary

This is a compact pedagogical Python repo for QuickSilver-style designated-verifier ZK proofs. The runtime package is intentionally stdlib-only, with cryptographic randomness from `secrets`, transcript/hash derivation through `hashlib`, and local arithmetic implementations in `quicksilver/field.py` and `quicksilver/gf2k.py`. The main dependency risk is not hidden third-party code; it is the absence of dependency metadata, Python-version metadata, install metadata, and a stable command surface.

The README claim that the repo has no third-party dependencies is true for production modules, but not for the whole checkout: the tests require `pytest`. The README command spelling also assumes a `python` executable, which is absent in this worker environment; the same tests pass with `python3`. There is also a stale doc/demo mismatch: README says six runnable demos, but `git ls-files demos` shows five demo files, and the referenced `demos/transitive_closure.py` lives in sibling `tensor-logic`, not this repo.

Only this report was added. No product code, tests, generated data, secrets, external services, deploys, pushes, or PRs were touched.

## Current State and Evidence

- `git branch --show-current` -> `codex/goal-tensor-quicksilver-zk-dependency-surface`.
- `git rev-parse HEAD` -> `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.
- Initial `git status --short` -> empty output, so the worktree was clean before this report.
- `rg --files -uu` found only `.gitignore`, `README.md`, `quicksilver/`, `tests/`, `demos/`, and the `.git` worktree pointer.
- `git ls-files | wc -l` -> `27` tracked files.
- `git ls-files demos` -> five files: `demos/lpn_vole_demo.py`, `demos/quicksilver_boolean_demo.py`, `demos/quicksilver_demo.py`, `demos/zk_einsum.py`, `demos/zk_graph_reachability.py`.
- `python --version` failed: `/opt/homebrew/bin/bash: line 1: python: command not found`.
- `python3 --version` -> `Python 3.12.8`.
- `python -m pytest tests/ -q` failed for the same missing `python` shim.
- `python3 -m pytest tests/ -q` -> `76 passed in 0.44s`.
- `python3 -m pytest --collect-only -q tests/` -> `76 tests collected in 0.10s`.
- `git status --short --ignored` after tests showed ignored local cache `!! .pytest_cache/`; `.gitignore` ignores `.pytest_cache/`, `__pycache__/`, `*.pyc`, `.venv/`, and `*.egg-info/`.
- `git remote -v` points to `https://github.com/jwalin-shah/quicksilver-zk.git`.

## Dependency Inventory

### Declared Dependencies

There are no dependency declaration files in this checkout. `git ls-files` and `fd` found no:

- `pyproject.toml`
- `setup.py`
- `setup.cfg`
- `requirements*.txt`
- `Pipfile`
- `poetry.lock`
- `uv.lock`
- `tox.ini`
- `noxfile.py`
- `Makefile`
- `Dockerfile`
- `.github/` workflow files
- `.env` files

Implication: a future worker can run the package directly from the repo root, but cannot install it as a package, infer a supported Python range, or ask a tool like `uv`, `pip`, or CI to provision the repo from metadata.

### Runtime Imports

Production modules use only Python stdlib plus internal `quicksilver.*` imports:

- `quicksilver/field.py:14` imports `secrets`; `F.rand()` uses `secrets.randbits` for rejection sampling.
- `quicksilver/gf2k.py:16` imports `secrets`; `GF2k.rand()` uses `secrets.randbits(128)`.
- `quicksilver/lpn_vole.py:51-52` imports `hashlib` and `secrets`; matrix derivation uses SHA-256 counter mode and base VOLE uses `secrets.SystemRandom`.
- `quicksilver/fiat_shamir.py:28` imports `hashlib`; transcript challenge generation uses SHA-256.
- `quicksilver/circuit.py`, `quicksilver/boolean.py`, `quicksilver/protocol.py`, `quicksilver/polynomial.py`, and `quicksilver/zk_reachability.py` depend on stdlib `dataclasses`, `enum`, `typing`, and `itertools`.
- `quicksilver/__init__.py:12-17` exports only prime-field APIs (`F`, `Fp`, `Wire`, `Circuit`, `prove`, `verify`, `run`), not boolean, LPN, Fiat-Shamir, einsum, or reachability helpers.

No production file imports `numpy`, `torch`, `requests`, `cryptography`, `networkx`, `subprocess`, `socket`, `json`, `yaml`, `toml`, `pickle`, or filesystem IO helpers.

### Test and Demo Imports

- All test files import `pytest`; this is the only observed third-party dependency.
- Test files and demos add the repo root to `sys.path` manually, e.g. `tests/test_lpn_vole.py:5-8` and each demo's `sys.path.insert(...)` block. This compensates for the lack of packaging metadata.
- Demos use stdlib `os`, `sys`, and `time`; `demos/zk_graph_reachability.py` also uses `collections.deque`, `typing`, and local `random.Random(seed=...)`.

### Python Version Surface

The code uses Python 3.10+ syntax:

- `int | None` in `quicksilver/circuit.py:53`, `quicksilver/vole.py:50`, `quicksilver/boolean.py:62`, and `quicksilver/lpn_vole.py:140`.
- Built-in generics such as `tuple[list[str], str]` in `quicksilver/einsum.py:46`.
- Type union assignment `_Slot = _Public | _Wire` in `quicksilver/zk_reachability.py:177`.

Observed pass environment is Python 3.12.8. There is no declared `requires-python`, so Python 3.9 and older will fail syntactically, and Python 3.10/3.11 are unverified in this audit.

## Entrypoints and Scripts

README-documented entrypoints:

- `python -m pytest tests/ -v` in `README.md:167`.
- `python demos/quicksilver_demo.py` in `README.md:170`.
- `python demos/zk_graph_reachability.py` in `README.md:171`.
- `python demos/zk_einsum.py` in `README.md:172`.
- `python demos/quicksilver_boolean_demo.py` in `README.md:175`.
- `python demos/lpn_vole_demo.py` in `README.md:178`.

Observed executable equivalents under this worker's shell:

- `python3 -m pytest tests/ -q` passed.
- `python3 demos/quicksilver_demo.py` passed and printed `All demos passed.`
- `python3 demos/quicksilver_boolean_demo.py` passed and printed `All boolean QuickSilver demos passed.`
- `python3 demos/zk_einsum.py` passed and printed `All einsum-ZK demos passed.`
- `python3 demos/zk_graph_reachability.py` passed and printed `All ZK reachability demos passed.`
- `python3 demos/lpn_vole_demo.py` passed and printed `All LPN-VOLE demos passed.`

There are no CLI wrappers, no package entrypoints, no Make targets, and no CI workflow files. The cheap command surface is therefore implicit and README-driven.

## Generated Artifacts, Caches, and Local State

- `.gitignore` ignores `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`, and `*.egg-info/`.
- Running pytest produced an ignored `.pytest_cache/` entry, visible only with `git status --short --ignored`.
- No committed generated artifacts were found in this checkout.
- No local env files or secrets were found.
- No code path searched reads or writes files, shells out, opens sockets, or calls external services.

## Cryptographic and Randomness Surface

The repo is educational but uses cryptographic-looking primitives. Dependency risk here is mostly stale assumptions and missing threat-boundary metadata:

- `README.md:10-11` claims no third-party dependencies and high soundness bounds.
- `quicksilver/field.py:68-69` hardcodes the Mersenne prime `2^127 - 1`.
- `quicksilver/gf2k.py:8-11` explicitly says the pure-Python GF(2^128) multiply is not production-grade and should be replaced with a faster primitive for serious use.
- `quicksilver/vole.py:12-16` documents trusted-dealer VOLE as a model, not a deployment-ready preprocessing protocol.
- `quicksilver/lpn_vole.py:36-46` documents missing base OT/SPCOT and says default LPN parameters are not secure.
- `quicksilver/fiat_shamir.py:9-12` states Fiat-Shamir remains designated-verifier, not public verification.

This is clear inside source docstrings, but not captured in install metadata, package classifiers, or automated checks.

## Validation Map

Commands actually run:

- `git status --short` before report: expected empty, observed empty.
- `python --version`: expected fail in this environment, observed `python: command not found`.
- `python -m pytest tests/ -q`: expected fail in this environment, observed `python: command not found`.
- `python3 --version`: expected pass, observed `Python 3.12.8`.
- `python3 -m pytest tests/ -q`: expected pass, observed `76 passed in 0.44s`.
- `python3 -m pytest --collect-only -q tests/`: expected pass, observed `76 tests collected in 0.10s`.
- `python3 demos/quicksilver_demo.py`: expected pass, observed pass.
- `python3 demos/quicksilver_boolean_demo.py`: expected pass, observed pass.
- `python3 demos/zk_einsum.py`: expected pass, observed pass.
- `python3 demos/zk_graph_reachability.py`: expected pass, observed pass.
- `python3 demos/lpn_vole_demo.py`: expected pass but slower, observed pass with the `n_out=2048` timing around `20045.1 ms`.

Validation command for this queue item:

- `git status --short`: expected to exit successfully and show only the report directory as untracked after the write. Observed final output: `?? docs/`.
- `git status --short -uall`: expected to reveal the exact untracked report path. Observed final output: `?? docs/overnight/tensor-quicksilver-zk-dependency-surface.md`.

Recommended future validation candidates:

- `python3 -m pytest tests/ -q`: should pass; proves the full observed test suite.
- `python3 -m pytest --collect-only -q tests/`: should pass; cheap way to detect collection/import dependency breakage.
- `python3 demos/quicksilver_demo.py && python3 demos/zk_einsum.py`: should pass; cheap demo smoke for arithmetic and tensor-logic frontends.
- `python3 demos/lpn_vole_demo.py`: should pass but is not cheap; keep as optional or shrink the scaling loop before making it a standard fast check.
- `python -m pytest tests/ -q`: should fail in this worker unless a `python` shim is added; useful only as a README portability check.

## Risks and Stale Assumptions

1. README command portability is stale. The documented `python ...` commands fail here because only `python3` exists. This affects tests and all demos as written in `README.md:167-178`.
2. Packaging metadata is absent. There is no `pyproject.toml` or requirements file, so `pytest` is undeclared, supported Python versions are undeclared, and the package cannot be installed normally.
3. README demo count is stale. `README.md:10-11` and `README.md:93` say six runnable demos, but the repo tracks five demo files.
4. README references a missing local file. `README.md:185` mentions `demos/transitive_closure.py`, but that file is not present in this repo; it exists in sibling `tensor-logic`.
5. Test importability depends on path mutation. Every test file and demo manually edits `sys.path`, which hides packaging issues and can produce different behavior from installed-package use.
6. Security parameters are educational. `quicksilver/lpn_vole.py:43-46` says default LPN parameters are not secure; `README.md` should keep that boundary impossible to miss for users who run the LPN demo.
7. Runtime cost is not bounded by a fast validation profile. The LPN demo's `n_out=2048` case took about 20 seconds locally, which is too slow for a default smoke check despite being valuable as a scaling observation.
8. Public API surface is narrower than module surface. `quicksilver/__init__.py` exports prime-field basics only; users following README snippets import advanced helpers from module paths directly.

## Sibling Repo Comparison

`repos.json` lists related tensor repos:

- `tensor-experiments`
- `tensor-fafsa-engine`
- `tensor-quicksilver-zk`
- `tensor-taxes`
- `tensor-logic`

The closest sibling is `tensor-logic`:

- `/Users/jwalinshah/projects/tensor/tensor-logic/pyproject.toml:10-20` declares Python `>=3.11`, runtime `torch>=2.0`, and dev dependencies `matplotlib`, `numpy`, and `pytest`.
- `/Users/jwalinshah/projects/tensor/tensor-logic/demos/transitive_closure.py:1-10` contains the exact transitive-closure/einsum framing referenced from this repo's README.
- `/Users/jwalinshah/projects/tensor/tensor-logic/demos/transitive_closure.py:13` imports `torch`; the QuickSilver repo reimplements its ZK-facing einsum compiler in `quicksilver/einsum.py` without taking a `torch` dependency.
- The sibling `tensor-logic` checkout was dirty during this read-only comparison (`git status --short` showed modified files and untracked `CLAIMS.md` / `docs/remote-jobs/`), so this audit did not rely on it as a stable validation source.

Overlap/handoff risk: QuickSilver's README borrows a Tensor Logic concept and filename from `tensor-logic`, but this repo does not declare that sibling as a dependency or submodule. Morning reviewers should treat the relationship as conceptual, not executable.

## Next Safe Work

### Task 1: Add Minimal Python Packaging Metadata

Acceptance criteria:

- Add `pyproject.toml` with `requires-python` matching the syntax floor, likely `>=3.10` or `>=3.11`.
- Declare runtime dependencies as empty and dev/test dependency as `pytest`.
- Preserve current direct-from-repo execution.
- Do not add product dependencies.

Validation:

- `python3 -m pytest tests/ -q` should pass.
- `python3 -m pip install -e .[dev]` should succeed in a disposable venv.
- `python3 -c "import quicksilver; print(quicksilver.__all__)"` should succeed.

### Task 2: Normalize README Commands and Demo Claims

Acceptance criteria:

- README uses `python3` or documents `python` vs `python3` clearly.
- Demo count matches `git ls-files demos`.
- The `demos/transitive_closure.py` reference is either linked as sibling `tensor-logic` context or removed as a local-file claim.
- The test command remains exactly reproducible.

Validation:

- `python3 -m pytest tests/ -q` should pass.
- `for f in demos/*.py; do python3 "$f"; done` should pass, or README should mark the long LPN scaling demo separately.
- `rg -n "six runnable demos|demos/transitive_closure.py|python -m pytest|python demos/" README.md` should show no stale local command claims.

### Task 3: Add a Cheap Validation Profile

Acceptance criteria:

- Introduce a lightweight script or Make target for fast local proof, without adding product dependencies.
- It should run full tests and a small demo subset.
- It should avoid the 20-second LPN `n_out=2048` scaling case unless explicitly requested.

Validation:

- New fast command should pass in under a few seconds on Python 3.12 in this environment.
- Full optional demo command should still pass when run manually.
- `git status --short --ignored` should not expose unexpected unignored generated files.

### Task 4: Clarify Educational Cryptography Boundaries

Acceptance criteria:

- README highlights trusted-dealer setup, insecure default LPN params, designated-verifier verification, and pure-Python performance limits near the usage section, not only in source docstrings.
- No implementation behavior changes.

Validation:

- `python3 -m pytest tests/ -q` should pass.
- `rg -n "trusted dealer|not secure|designated-verifier|production|LPN" README.md quicksilver/*.py` should show the boundary in both README and source.

## Non-Goals

- No product code changes.
- No dependency upgrades or new runtime dependencies.
- No external research validation of the QuickSilver paper claims.
- No CI setup, GitHub Actions writes, pushes, or PR creation.
- No edits to sibling repos.
- No attempt to make the educational VOLE/LPN implementation production-ready.

## Unknowns

- Intended minimum Python version: syntax requires 3.10+, sibling `tensor-logic` uses `>=3.11`, and this audit only ran Python 3.12.8.
- Whether the repo is meant to become installable or stay script-only.
- Whether README should keep conceptual references to sibling `tensor-logic` or vendor a minimal `transitive_closure.py` demo here.
- Whether LPN scaling demo should remain a default demo despite its 20-second local `n_out=2048` case.
- Whether the public API should export boolean, LPN, Fiat-Shamir, einsum, and reachability helpers from `quicksilver/__init__.py`.

## Handoff

Changed files:

- `docs/overnight/tensor-quicksilver-zk-dependency-surface.md`

Commit/PR:

- No commit created.
- No PR created.
- HEAD remains `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.

Blockers:

- None for the audit report.
- Future packaging work needs a product decision on supported Python version and installability.

Final validation:

- `git status --short` completed successfully and reported only `?? docs/`.
