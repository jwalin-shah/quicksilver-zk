# tensor-quicksilver-zk validation-map audit

Queue item: `tensor-quicksilver-zk-validation-map`  
Repo path: `/Users/jwalinshah/projects/agent-stack/.agent-stack-worktrees/2026-05-07-overnight-marathon/tensor-quicksilver-zk-validation-map`  
Audit date: 2026-05-07  
Focus area: validation-map

## Executive summary

`tensor-quicksilver-zk` is a compact pedagogical Python implementation of QuickSilver-style zero-knowledge proof components. The working validation surface is real and fast when invoked with `python3`: `python3 -m pytest tests/ -q` collected and passed 76 tests in 0.45s, and all five local demo scripts passed. The repo is not packaged, has no checked-in dependency declaration, no CI workflow, and no lint/type/format commands. The README's literal `python ...` validation commands fail in this worker environment because `python` is not on PATH, while `python3` is available.

The safest near-term work is to make the validation contract explicit: add packaging/test metadata, document `python3` or a managed runner, add a cheap/full validation split, and fix stale README claims about demo count and the missing `demos/transitive_closure.py` reference.

## Repo purpose and state

- Purpose observed from `README.md`: pedagogical pure-Python QuickSilver zero-knowledge proofs with prime-field circuits, boolean circuits over `GF(2^128)`, LPN VOLE extension, Fiat-Shamir, tensor-logic einsum compilation, and graph reachability demos.
- Current branch: `codex/goal-tensor-quicksilver-zk-validation-map`.
- Current HEAD at audit start: `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.
- Initial dirty state: `git status --short --branch` returned only `## codex/goal-tensor-quicksilver-zk-validation-map`; `git status --short` returned no output before this report was added.
- Product code was not edited. The only intended tracked change is this report at `docs/overnight/tensor-quicksilver-zk-validation-map.md`.

## Local evidence

- `llm-tldr tree .` shows a small repo with `quicksilver/`, `tests/`, `demos/`, `.gitignore`, and `README.md`; no `pyproject.toml`, `setup.py`, `requirements.txt`, `tox.ini`, `noxfile.py`, `Makefile`, or CI directory appears in the top-level tree.
- `rg --files` found 13 Python files in `quicksilver/`, 6 test files plus `tests/__init__.py`, 5 demo scripts, and `README.md`.
- `wc -l quicksilver/*.py tests/*.py demos/*.py README.md` reported 4,259 total lines: 2,279 lines under `quicksilver/`, 1,130 lines under `tests/`, 738 lines under `demos/`, and 212 lines in `README.md`.
- `README.md` line 167 documents `python -m pytest tests/ -v` as the test command and claims "76 passing in <1s".
- `python -m pytest tests/ -q` failed immediately with `/opt/homebrew/bin/bash: line 1: python: command not found`.
- `command -v python3` returned `/usr/local/bin/python3`; `python3 --version` returned `Python 3.12.8`.
- `python3 -m pytest --collect-only -q` collected 76 tests in 0.11s across `tests/test_boolean.py`, `tests/test_einsum.py`, `tests/test_fiat_shamir.py`, `tests/test_lpn_vole.py`, `tests/test_quicksilver.py`, and `tests/test_zk_reachability.py`.
- `python3 -m pytest tests/ -q` passed: `76 passed in 0.45s`.
- `python3 -m compileall -q quicksilver tests demos` exited 0 with no output.
- `python3 demos/quicksilver_demo.py` passed all factorisation, polynomial, and batched-check demos.
- `python3 demos/zk_graph_reachability.py` passed reachability, tampering, and size-scaling demos; output included a 16-vertex scaling case with 1,408 mul gates.
- `python3 demos/zk_einsum.py` passed matmul, grandparent-rule, and closure-step demos.
- `python3 demos/quicksilver_boolean_demo.py` passed boolean multiplier and XOR-mixer demos; the 10-bit scaling row took about 245 ms locally.
- `python3 demos/lpn_vole_demo.py` passed but is not a cheap smoke command: its final setup row printed `n_out=2048`, `k_base=4096`, and about `20531.1 ms`.
- `.gitignore` ignores `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`, and `*.egg-info/`; after tests/demos/compileall, ignored cache directories existed under `.pytest_cache`, `tests/__pycache__`, `quicksilver/__pycache__`, and `demos/__pycache__`, while `git status --short` still returned no output before report creation.

## Validation inventory

| Command | Observed status | Notes |
| --- | --- | --- |
| `git status --short` | Pass, exit 0 | Required queue validation command. Before this report, output was empty. After this report, default output is `?? docs/`; `--untracked-files=all` shows the report path. |
| `python -m pytest tests/ -q` | Fail in this worker | `python` is absent from PATH. This is an environment/README command problem, not a test failure. |
| `python3 -m pytest --collect-only -q` | Pass | Collected 76 tests in 0.11s. Good cheap discovery check. |
| `python3 -m pytest tests/ -q` | Pass | 76 passed in 0.45s. Best current local proof command. |
| `python3 -m pytest tests/ -v` | Expected pass | README command shape, but should use `python3` or a managed runner in this environment. |
| `python3 -m compileall -q quicksilver tests demos` | Pass | Useful syntax/import smoke; no lint semantics. |
| `python3 demos/quicksilver_demo.py` | Pass | Good prime-field demo smoke. |
| `python3 demos/zk_einsum.py` | Pass | Good tensor-logic/ZK integration smoke. |
| `python3 demos/zk_graph_reachability.py` | Pass | Useful but slightly heavier integration/scaling smoke. |
| `python3 demos/quicksilver_boolean_demo.py` | Pass | Useful boolean `GF(2^128)` smoke. |
| `python3 demos/lpn_vole_demo.py` | Pass but slow | Last row took about 20.5s locally; keep in full validation, not quick validation. |
| `ruff check .` | No local contract | No `pyproject.toml`, `ruff.toml`, or README claim found. |
| `mypy .` | No local contract | No type-check config or dependency metadata found. |
| `coverage run -m pytest` | No local contract | No coverage config or threshold found. |

## Test surface map

- `tests/test_quicksilver.py` has 18 tests covering prime-field arithmetic, trusted-dealer VOLE correlation, IT-MAC relation preservation, protocol completeness, polynomial checks, and tampered proof rejection.
- `tests/test_boolean.py` has 17 tests covering `GF(2^128)` arithmetic, subspace VOLE correlation, boolean circuit completeness, wrong-witness rejection, and tampered batched/assertion checks.
- `tests/test_einsum.py` has 15 tests covering einsum parsing, dimension validation, plain evaluation, circuit compilation, public tensor inputs, wrong output rejection, flattening, and the grandparent-rule tie-in.
- `tests/test_fiat_shamir.py` has 8 tests covering non-interactive completeness, deterministic proof under fixed setup, tamper rejection, label binding, transcript squeeze independence, polynomial circuit support, and assertion-time wrong witness rejection.
- `tests/test_lpn_vole.py` has 11 tests covering LPN VOLE correlation, output length, supplied delta, deterministic matrix derivation, seed variance, sparse-base hiding sanity, protocol/polynomial integration, tamper rejection, and parameter guard rails.
- `tests/test_zk_reachability.py` has 7 tests covering path completeness, cyclic walks, witness-assembly rejection, malicious edge claims, post-commit tampering, and `n^2*k` gate-count sanity.
- Each test file inserts the repo root into `sys.path`; this helps direct checkout execution but hides the lack of install/package validation.

## Entrypoints and validation-relevant modules

- `quicksilver/circuit.py` defines `Circuit` and `vole_count()` as `num_inputs + num_muls + 1`, which is exercised by protocol, polynomial, LPN, and reachability tests.
- `quicksilver/protocol.py` exposes `prove`, `verify`, and `run`; tests hit both high-level `run` and lower-level tampering paths.
- `quicksilver/boolean.py` exposes `BoolCircuit`, boolean `trusted_dealer_setup`, `prove`, `verify`, and `run`; tests cover both arithmetic and protocol behavior.
- `quicksilver/fiat_shamir.py` exposes `Transcript`, `prove_ni`, `verify_ni`, and `run_ni`; tests cover transcript label binding and tampered message rejection.
- `quicksilver/lpn_vole.py` exposes `LpnParams`, `derive_matrix`, `lpn_vole_extend`, and `correlation_holds`; tests cover correctness but not real security parameter validation.
- `quicksilver/einsum.py` exposes `assert_einsum_equals`, `evaluate_einsum`, tensor allocation, and flattening helpers; tests cover compile/evaluate shapes but not large randomized tensor specs.
- `quicksilver/zk_reachability.py` exposes `build_circuit`, `assemble_witness`, and `prove_path`; tests cover a few positive/negative graph shapes and one scaling assertion.
- `demos/*.py` are all executable with `python3` and include their own `sys.path.insert(...)` checkout bootstrapping.

## Risks and stale assumptions

1. The documented validation command is not portable in this environment. `README.md` uses `python`, but this worker only has `python3`; the literal README command fails before pytest starts.
2. There is no machine-readable project metadata. The repo depends on `pytest` for tests but has no `pyproject.toml`, `requirements-dev.txt`, or lockfile, so another worker cannot recreate the validated environment from the repo alone.
3. There is no CI, Makefile, tox/nox config, or checked-in validation script. The validation contract currently lives in README prose and this audit report, not executable repo policy.
4. README claims are stale or ambiguous: it says "Eight modules" while `quicksilver/` currently contains 13 `.py` files including `__init__.py`; it says "six runnable demos" while the checkout has five demo scripts; it references `demos/transitive_closure.py`, which is absent from this repo.
5. Tests use fresh randomness from `secrets` and `F.rand*` in several places without deterministic seeding. The observed suite passed, and collision probabilities are tiny, but failures would be hard to reproduce from a seed.
6. Demo validation is uneven. Four demos are cheap enough for a smoke run, but `demos/lpn_vole_demo.py` includes a 20s local setup row and should not be part of the default quick validation.
7. No lint/type/format command exists, so syntax and tests can pass while style, unused code, import hygiene, or type-regression issues remain invisible.
8. Installability is untested. Tests and demos work by adding the checkout root to `sys.path`; there is no proof that `pip install -e .`, build backends, package data, or public imports work from outside the repo root.

## Sibling repo comparison

The Goal Pack inventory at `/Users/jwalinshah/projects/agent-stack/repos.json` lists related `tensor` repos including `tensor-logic` and `tensor-quicksilver-zk`. I did a read-only comparison only.

- `repos.json` records `tensor-quicksilver-zk` with validation `git status --short`, while `tensor-logic` has validation `python3 -m pytest -q`.
- `/Users/jwalinshah/projects/tensor/tensor-logic` has a `pyproject.toml` with `pytest>=8.0` and pytest config; this repo has no equivalent metadata.
- `tensor-logic` has `tests/test_packaging_ci.py`, including checks that worker validation commands are documented. This repo has no packaging/CI validation tests.
- `tensor-logic` contains `demos/transitive_closure.py`; this repo's README references that path, but the file is not present here. This looks like conceptual reuse from the tensor-logic repo without a local artifact.
- `tensor-logic` was dirty when inspected (`CLAUDE.md`, `tensor_logic/ingest.py`, multiple tests, web workbench files, `CLAIMS.md`, and `docs/remote-jobs/`), so I did not run its validation or inspect further.

## Next safe work

1. Add explicit Python project metadata.
   - Acceptance criteria: add `pyproject.toml` with package metadata, Python version floor, pytest dev dependency, and pytest discovery config; remove or justify per-test `sys.path.insert` if editable install covers it.
   - Validation: `python3 -m pip install -e '.[dev]'`, `python3 -m pytest tests/ -q`, `python3 -m compileall -q quicksilver tests demos`.

2. Add a checked-in validation runner.
   - Acceptance criteria: add `scripts/validate_quick.sh` or `Makefile` target for quick proof (`pytest` plus compileall), and a full target that includes demos while marking `demos/lpn_vole_demo.py` as slow.
   - Validation: `bash scripts/validate_quick.sh`; `bash scripts/validate_full.sh` or `make validate-full` if a Makefile is chosen.

3. Fix README validation and inventory claims.
   - Acceptance criteria: README says `python3` or a repo-managed runner, lists the actual five local demo files, removes or relocates the missing `demos/transitive_closure.py` reference, and updates module-count prose to match `quicksilver/`.
   - Validation: `python3 -m pytest tests/ -q`; `rg -n "python -m|six runnable|Eight modules|demos/transitive_closure.py" README.md` should show no stale local claims unless intentionally explained.

4. Add deterministic smoke tests for validation-critical randomness paths.
   - Acceptance criteria: tests for `F.rand*` consumers and LPN matrix derivation include fixed-seed or fixed-delta cases sufficient to reproduce failures; randomized tests remain as supplemental checks.
   - Validation: `python3 -m pytest tests/test_lpn_vole.py tests/test_quicksilver.py tests/test_boolean.py -q`.

5. Add CI once the local validation command is explicit.
   - Acceptance criteria: a workflow runs the quick validation command on push/PR for at least the supported Python version; if full demos are included, slow demo is separated or timeout-controlled.
   - Validation: local `python3 -m pytest tests/ -q` plus CI dry-read of workflow YAML; actual remote CI run would require GitHub push/PR and is outside this queue item.

## Non-goals

- No product code changes.
- No generated data changes.
- No secret, credential, deployment, or external service work.
- No push, PR, or tracker state transition.
- No attempt to prove cryptographic security of the implementation.
- No sibling repo mutation; sibling comparison was read-only.

## Unknowns

- Supported Python version range is not declared. The local proof used Python 3.12.8 only.
- Whether the repo should intentionally remain unpackaged is unknown; current tests assume checkout-root execution.
- Whether `pytest` is expected to be globally installed or provisioned by a tool such as `uv`, `pipx`, or a virtualenv is unknown.
- Whether the missing `demos/transitive_closure.py` reference should be copied from `tensor-logic`, linked as a sibling concept, or removed from this repo is a product/docs judgment.
- No remote CI or GitHub metadata was inspected, because this queue item is local and read-only aside from the report.
