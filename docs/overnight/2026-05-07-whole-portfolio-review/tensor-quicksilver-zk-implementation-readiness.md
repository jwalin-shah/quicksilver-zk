# tensor-quicksilver-zk implementation-readiness review

Date: 2026-05-07
Branch: `codex/goal-tensor-quicksilver-zk-implementation-readiness`
Review pass: `implementation-readiness`
Start HEAD: `60b7fbe`

Scope: read-only repo review and queue prep. Product code was not edited; this report is the only intended repo change.

## Readiness verdict

This repo is ready for small, executable follow-up issues around packaging, CI, documentation drift, malformed-input handling, LPN parameter safety, and cost-model regression coverage. It is not ready to treat as production cryptography: the repo self-identifies as pedagogical, still uses trusted-dealer/base VOLE in key paths, lacks package/CI metadata, and has stale demo/docs claims.

## Evidence inventory

- `llm-tldr tree .` found a small Python repo with `README.md`, `quicksilver/`, `tests/`, and `demos/`.
- `rg --files -g '!*__pycache__*'` found 13 package modules, 6 test files, 5 demo files, and no pre-existing `docs/` report tree.
- `find . -maxdepth 3` found no `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`, `tox.ini`, `noxfile.py`, `pytest.ini`, `ruff.toml`, `.pre-commit-config.yaml`, `.github` workflow, `AGENTS.md`, or `CLAUDE.md`.
- `find .. -maxdepth 4 -path '*overnight*' -type f` found only sibling runner docs, not repo-local previous overnight outputs for this repo.
- Initial `git status --short --branch` showed the expected branch and no dirty files before the report was written.

## Concrete file-path observations

1. `README.md:10-13` says the repo has "Eight modules, 76 tests, six runnable demos", but file inventory shows 13 `quicksilver/*.py` modules and 5 `demos/*.py` files. The test count is accurate; the module and demo counts are stale.
2. `README.md:76-93` lists the intended package/test/demo layout and is still the best entrypoint, but it does not match the current package surface: `boolean.py`, `fiat_shamir.py`, `einsum.py`, and `zk_reachability.py` are present and important enough to drive follow-up work.
3. `README.md:164-178` documents `python -m pytest tests/ -v` and `python demos/...` commands. In this workspace, `python -m pytest tests/ -q` failed because `python` is not on PATH; `python3 -m pytest tests/ -q` passed.
4. `README.md:181-188`, `demos/zk_einsum.py:3-4`, `demos/zk_graph_reachability.py:3`, and `quicksilver/zk_reachability.py:41-44` reference `transitive_closure.py` and `train_kg.py`, but no such local files exist in `rg --files`. That makes the tensor-logic narrative hard for the next implementer to verify locally.
5. `quicksilver/circuit.py:21-28` and `quicksilver/circuit.py:115-117` provide a crisp cost contract: VOLE consumption is `num_inputs + num_muls + 1`, with one trailing mask. This is a good basis for gate-count regression tests.
6. `quicksilver/protocol.py:79-90` and `quicksilver/protocol.py:171-211` consume VOLE/message iterators with `next(...)`; malformed shares or truncated `CommitMessage.d_values` can raise implementation exceptions instead of producing a clean verifier rejection.
7. `quicksilver/protocol.py:132-154` and `quicksilver/protocol.py:222-233` implement the prime-field batched multiplication check directly and match the README's algebra. Existing tests cover honest runs and several tampering cases, so malformed-input hardening can be scoped without changing the algebra.
8. `quicksilver/boolean.py:1-27` mirrors the QuickSilver protocol over boolean wires and GF(2^128), and `quicksilver/boolean.py:217-285` implements the prover path. Like the prime-field path, it consumes iterators directly and should get the same malformed-input treatment.
9. `quicksilver/fiat_shamir.py:18-24` documents the need to bind circuits into Fiat-Shamir transcripts, and `quicksilver/fiat_shamir.py:78-95` serializes circuit shape and gates. This is implementation-ready for stronger regression tests around transcript incompatibility and canonical serialization.
10. `quicksilver/polynomial.py:1-33` describes the degree-d polynomial extension and `quicksilver/polynomial.py:126-167` implements masked prover coefficients. The feature is covered by core tests, but it is not surfaced in the package `__all__` or packaging metadata because package metadata does not exist.
11. `quicksilver/lpn_vole.py:36-46` explicitly says base OT/SPCOT is absent and default parameters are not secure; `quicksilver/lpn_vole.py:67-72` still exposes `LpnParams.default(...)`. That is acceptable for a demo, but unsafe as a future default API without a clearer name or guardrail.
12. `quicksilver/einsum.py:21-34` states the compiler materializes contractions explicitly with no optimization passes; `quicksilver/einsum.py:102-149` implements the lowering. This makes optimization work separable from correctness work.
13. `quicksilver/zk_reachability.py:31-39` states reachability costs roughly scale as `n^2 * k`, and `quicksilver/zk_reachability.py:79-103` builds booleanity, one-hot, and step constraints. This is ready for formula-level regression tests that avoid flaky timing thresholds.
14. `tests/test_quicksilver.py:89-140` covers core completeness for single multiplication, linear-only circuits, polynomial circuits, and many multiplications; `tests/test_quicksilver.py:155-238` covers assertion tampering and batched-check tampering.
15. `tests/test_einsum.py:27-71` covers parsing, dimension consistency, and reference evaluation; `tests/test_einsum.py:87-147` covers compiled proof success and wrong-output rejection.
16. `tests/test_lpn_vole.py:26-42` verifies LPN VOLE correlation correctness and supplied delta behavior; `tests/test_lpn_vole.py:77-120` verifies LPN output plugs into the protocol and preserves tamper rejection.
17. `tests/test_zk_reachability.py:31-64` covers honest reachability and witness assembly rejection; `tests/test_zk_reachability.py:67-120` covers malicious path/tamper rejection; `tests/test_zk_reachability.py:123-134` checks asymptotic monotonicity.
18. `.gitignore:1-5` ignores `__pycache__`, `*.pyc`, `.pytest_cache/`, `.venv/`, and `*.egg-info/`, so the local pytest run did not dirty the worktree.

## Validation commands and results

- `python -m pytest tests/ -q`
  - Result: failed in this workspace because `/opt/homebrew/bin/bash: line 1: python: command not found`.
- `python3 -m pytest tests/ -q`
  - Result: passed, `76 passed in 0.45s`.
- Required queue validation command:
  - `git status --short`
  - Final handoff should record the exact output after this report is committed or left staged.

## Risks and blockers

- Packaging is missing. Without `pyproject.toml` or equivalent, external workers have no authoritative Python version, test runner, package name, or optional tooling contract.
- CI is missing. There is no `.github/workflows` gate to prove the 76 tests on fresh checkouts.
- README/demo inventory is stale. The current docs point at missing tensor-logic files and report wrong module/demo counts.
- The repo documents itself as pedagogical and non-production. `vole.py` uses a trusted dealer, and `lpn_vole.py` explicitly lacks base OT/SPCOT and secure parameter selection.
- Verifier/prover APIs are not yet hardened against malformed lengths. Current tests check value tampering, not truncated/extra protocol messages or VOLE shares.
- Performance claims are mostly narrative. There are gate-count checks, but no maintained benchmark or deterministic cost-model table for the frontend paths.

## Implementation-ready follow-up tasks

### 1. Add Python project metadata and a stable local runner

Owned files: `pyproject.toml`, `README.md`, optionally `tests/__init__.py` and test imports if editable install removes the need for `sys.path` hacks.

Acceptance criteria:
- `python3 -m pip install -e .` works in a fresh virtualenv.
- `python3 -m pytest tests/ -q` remains green.
- README run commands use an interpreter command that works on macOS/Linux workers, or document the required alias explicitly.
- Test files no longer need repo-root `sys.path.insert(...)` if editable install is the supported path.

Smallest useful validation:
- `python3 -m pip install -e .`
- `python3 -m pytest tests/ -q`
- `python3 -c "from quicksilver import Circuit, run; c=Circuit(); x=c.input(); c.assert_eq(x, 3); assert run(c, [3])"`

### 2. Add CI for tests and demo smoke checks

Owned files: `.github/workflows/tests.yml`, `pyproject.toml`, `README.md`.

Acceptance criteria:
- CI runs on pull requests and pushes to the default branch.
- CI tests at least one current Python 3 version and one upcoming/stable adjacent version.
- CI runs `python3 -m pytest tests/ -q`.
- CI runs one cheap demo smoke command, or clearly records why demos are excluded from the gate.

Smallest useful validation:
- `python3 -m pytest tests/ -q`
- `python3 demos/quicksilver_demo.py`

### 3. Repair README and demo narrative drift

Owned files: `README.md`, `demos/zk_einsum.py`, `demos/zk_graph_reachability.py`, `quicksilver/zk_reachability.py`, optionally new `demos/transitive_closure.py` if the intended file should be restored.

Acceptance criteria:
- README module and demo counts match `rg --files`.
- Every local file referenced by README/demo prose either exists or is explicitly described as external/historical context.
- The tensor-logic story remains intact without requiring hidden portfolio memory.

Smallest useful validation:
- `rg -n "transitive_closure|train_kg|six runnable demos|Eight modules" README.md quicksilver demos tests`
- `python3 -m pytest tests/ -q`

### 4. Harden malformed protocol input handling

Owned files: `quicksilver/protocol.py`, `quicksilver/boolean.py`, `tests/test_quicksilver.py`, `tests/test_boolean.py`.

Acceptance criteria:
- Prime-field `verify(...)` rejects truncated or extra `CommitMessage.d_values`, `assert_openings`, verifier shares, and batched messages without leaking `StopIteration`.
- Boolean `verify(...)` gets equivalent malformed-message coverage and rejects invalid non-bit `d_values` if that boundary is intended to be public.
- `prove(...)` reports too-short VOLE shares with clear `ValueError` messages.
- Existing honest and tamper tests remain green.

Smallest useful validation:
- `python3 -m pytest tests/test_quicksilver.py::test_soundness_tampered_batched_check_caught tests/test_boolean.py::test_soundness_tampered_batched_check_caught -q`
- `python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py -q`

### 5. Make LPN VOLE parameter safety explicit

Owned files: `quicksilver/lpn_vole.py`, `tests/test_lpn_vole.py`, `README.md`, `demos/lpn_vole_demo.py`.

Acceptance criteria:
- Demo-only defaults are named or gated so they cannot be mistaken for concrete security parameters.
- README and demo output state whether the selected parameters are demo-only or security-targeted.
- Tests cover both demo parameter construction and rejection/absence of unsupported production security levels.
- Existing LPN drop-in protocol tests still pass.

Smallest useful validation:
- `python3 -m pytest tests/test_lpn_vole.py -q`
- `python3 demos/lpn_vole_demo.py`

