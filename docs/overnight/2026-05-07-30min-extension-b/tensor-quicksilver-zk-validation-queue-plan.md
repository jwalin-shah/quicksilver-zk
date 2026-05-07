# tensor-quicksilver-zk second-pass validation and queue-readiness audit

Queue item: `tensor-quicksilver-zk-validation-queue-plan`  
Branch: `codex/goal-tensor-quicksilver-zk-validation-queue-plan`  
Repo path: `/Users/jwalinshah/projects/agent-stack/.agent-stack-worktrees/2026-05-07-30min-extension-b/tensor-quicksilver-zk-validation-queue-plan`  
HEAD: `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`  
Scope: read-only planning/synthesis except for this report. No product code, tests, demos, external services, trackers, pushes, merges, or PRs were changed.

## Executive summary

The repo is locally healthy when invoked with `python3`: collection finds 76 tests, the full test suite passes, and all five demo files run. The queue is not ready for normal implementation fanout from this branch until the contract gaps are made explicit: there is no package metadata, no CI config, no validation runner, no linter/type command, no declared Python version, and README commands still assume `python`, which is absent in this worker shell.

This pass reconciles prior overnight and first-pass reports rather than restating them. The highest-value implementation queue remains:

1. Reject zero verifier challenges in direct verifier APIs.
2. Harden message/share shape validation.
3. Promote or review the existing validation-runner follow-up branch instead of reimplementing packaging work.
4. Fix stale README inventory and security-boundary wording.
5. Make boolean witness handling strict.

## Prior-report reconciliation

I found and read these earlier tensor-quicksilver-zk reports in sibling worktrees:

- `../../2026-05-07-30min-extension/tensor-quicksilver-zk-30min-action-plan/docs/overnight/2026-05-07-30min-extension/tensor-quicksilver-zk-action-plan.md`
- `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-validation-map/docs/overnight/tensor-quicksilver-zk-validation-map.md`
- `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-docs-claims/docs/overnight/tensor-quicksilver-zk-docs-claims.md`
- `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-risk-register/docs/overnight/tensor-quicksilver-zk-risk-register.md`
- `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-dependency-surface/docs/overnight/tensor-quicksilver-zk-dependency-surface.md`
- `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-workflow-handoff/docs/overnight/tensor-quicksilver-zk-workflow-handoff.md`
- `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-architecture-map/docs/overnight/tensor-quicksilver-zk-architecture-map.md`

Reconciliation:

- The validation-map, dependency-surface, docs-claims, and workflow-handoff reports agree on the same local validation facts: `python3` works, `python` fails, tests pass, all five demos pass, LPN demo is slow, and no packaging/CI metadata exists in HEAD.
- The risk-register report adds the top implementation risk: direct verifier APIs accept caller-supplied `chi` and do not reject `chi == 0`; prior reproduction showed malicious prime and boolean transcripts accepting with zero challenge.
- The architecture-map report adds two important readiness tasks beyond docs/packaging: strict transcript/message/share shape validation and a deliberate committed-wire interface for polynomial-extension callers.
- The first 30-minute action plan already consolidated those reports and noted an implementation follow-up branch, `../../2026-05-07-implementation-followups/tensor-quicksilver-validation-runner`, at commit `c45b603`.
- I verified that follow-up branch exists, is clean, and already adds `pyproject.toml`, `Makefile`, `_quicksilver_build_backend.py`, and `tests/test_package.py`. Queue work should review/promote it before starting fresh packaging changes.

No `runs/*/result.json` or tensor-specific `runs/*/handoff.md` files were found in the searched extension/marathon worktree roots. Only unrelated template/handoff files appeared under other repos.

## Validation commands and observed results

| Command | Result | Queue-readiness note |
| --- | --- | --- |
| `git status --short --branch` | Passed; output `## codex/goal-tensor-quicksilver-zk-validation-queue-plan` before this report. | Correct isolated branch and clean tracked state at start. |
| `git rev-parse HEAD` | Passed; `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`. | Single initial commit is the baseline for all prior reports read. |
| `rg --files -uu` | Passed; found `.gitignore`, `README.md`, `quicksilver/`, `tests/`, `demos/`, and `.git` only. | No local docs/report directory before this report. |
| `fd -H '^(\\.github|pyproject\\.toml|setup\\.py|setup\\.cfg|tox\\.ini|noxfile\\.py|requirements.*|Makefile|pytest\\.ini|ruff\\.toml|mypy\\.ini|\\.pre-commit-config\\.yaml)$' .` | Passed with no output. | No CI, package metadata, test runner, linter config, type config, or dependency manifest in this branch. |
| `python -m pytest --collect-only -q` | Failed; `/opt/homebrew/bin/bash: line 1: python: command not found`. | README's `python ...` command spelling is not runnable in this worker environment. |
| `python -m pytest tests/ -q` | Failed; `/opt/homebrew/bin/bash: line 1: python: command not found`. | Same blocker; not a pytest failure. |
| `which python3` | Passed; `/usr/local/bin/python3`. | Use `python3` for local validation here. |
| `python3 -m pytest --collect-only -q` | Passed; `76 tests collected in 0.11s`. | Good cheap import/collection proof. |
| `python3 -m pytest tests/ -q` | Passed; `76 passed in 0.44s`. | Strongest current local proof command. |
| `python3 demos/quicksilver_demo.py` | Passed; printed `All demos passed.` | Good prime-field/polynomial demo smoke. |
| `python3 demos/quicksilver_boolean_demo.py` | Passed; printed `All boolean QuickSilver demos passed.`; 10-bit scaling row about 246.5 ms. | Good boolean smoke; still fast enough locally. |
| `python3 demos/lpn_vole_demo.py` | Passed; printed `All LPN-VOLE demos passed.`; largest scaling row `n_out=2048`, `k_base=4096`, about 20425.3 ms. | Keep out of default quick validation unless the slow scaling row is reduced or split. |
| `python3 demos/zk_einsum.py` | Passed; printed `All einsum-ZK demos passed.` | Good tensor/einsum integration smoke. |
| `python3 demos/zk_graph_reachability.py` | Passed; printed `All ZK reachability demos passed.`; `n=16,k=5` scaling row about 23.4 ms. | Good reachability integration smoke. |
| `git status --ignored --short` | Passed; output `!! .pytest_cache/` before this report. | Ignored pytest cache is the only generated artifact currently visible. |
| `fd -H 'tensor-quicksilver-zk.*\\.md|tensor-quicksilver-zk' /Users/jwalinshah/projects/agent-stack/.agent-stack-worktrees` | Passed; found prior reports and this worktree. | Confirms this is a second-pass reconciliation, not first-pass discovery. |
| `fd -H '^(result\\.json|handoff\\.md)$' ...` across the relevant extension/marathon roots | Passed; no tensor-specific result/handoff files found. | Morning review should still inspect runner-owned `runs/` if available outside these worktree roots. |

Required queue validation after this report:

- Command: `git status --short`
- Expected output after report creation: `?? docs/`
- Final observed output: `?? docs/`
- Exact untracked file check: `git status --short --untracked-files=all` reported `?? docs/overnight/2026-05-07-30min-extension-b/tensor-quicksilver-zk-validation-queue-plan.md`.

## Concrete file-path observations

1. `README.md` claims "Eight modules, 76 tests, six runnable demos." The 76-test claim is true, but current tracked inventory has 12 implementation modules excluding `quicksilver/__init__.py` and five demo files under `demos/`.
2. `README.md` documents `python -m pytest tests/ -v` and `python demos/...` commands. This worker has no `python` executable; all successful commands used `/usr/local/bin/python3`.
3. `README.md` references `demos/transitive_closure.py` in the tensor-logic tie-in. `rg --files` shows no such file in this repo; prior reports found the concept in sibling `tensor-logic`.
4. `.gitignore` ignores `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`, and `*.egg-info/`. After pytest and demos, `git status --ignored --short` reported only ignored `.pytest_cache/`.
5. `.github/workflows/*` is absent. There is no checked-in CI command, so queue readiness relies on local command prose and prior reports.
6. `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`, `tox.ini`, `noxfile.py`, `pytest.ini`, `Makefile`, `ruff.toml`, `mypy.ini`, and `.pre-commit-config.yaml` are absent in this branch. Tests require `pytest`, but the dependency is undeclared locally.
7. `tests/test_quicksilver.py` covers prime-field arithmetic, VOLE/IT-MAC correlation, protocol completeness, tampering, polynomial checks, and walker coherence. It hand-crafts malicious transcripts but still uses nonzero challenges in existing tamper checks.
8. `tests/test_boolean.py` covers GF(2^128), subspace VOLE, boolean completeness, wrong-witness rejection, tampered checks, and a 4-bit multiplier. It does not cover zero-challenge rejection or non-bit witness rejection.
9. `tests/test_einsum.py` covers parser/dimension validation, reference evaluation, circuit compilation, public tensor inputs, wrong-output rejection, flattening, and the local grandparent-rule proof. This is enough local evidence to replace the missing `demos/transitive_closure.py` README reference.
10. `tests/test_fiat_shamir.py` covers non-interactive completeness, deterministic proof with fixed setup, tamper rejection, label binding, transcript squeeze independence, polynomial-circuit support, and wrong-witness assertion rejection.
11. `tests/test_lpn_vole.py` covers LPN VOLE correlation, requested length, supplied delta, deterministic matrix derivation, seed variance, sparse-base hiding sanity, protocol/polynomial integration, tamper rejection, and parameter guard rails. It does not make demo defaults impossible to mistake for secure parameters.
12. `tests/test_zk_reachability.py` covers path completeness, cyclic walks, witness-assembly rejection, malicious non-edge witnesses, post-commit tampering, and monotonic circuit-size scaling. It does not expose a reusable cost estimator or validation limit for oversized caller inputs.
13. `quicksilver/__init__.py` exports only `F`, `Fp`, `Wire`, `Circuit`, `prove`, `verify`, and `run`. README examples import boolean, LPN, Fiat-Shamir, einsum, and reachability helpers from submodules, so API expansion is an explicit product decision.
14. `quicksilver/protocol.py` samples nonzero challenges only in the high-level `run(...)` helper; the lower-level `verify(..., chi, ...)` API accepts caller-provided challenges and prior risk-register reproduction showed `chi == 0` is a soundness footgun.
15. `quicksilver/boolean.py` mirrors the public caller-supplied challenge pattern and also coerces witness inputs with low-bit masking, which can hide caller bugs.
16. `quicksilver/polynomial.py` is architecturally beside the prime protocol and works over committed wire dictionaries. Tests need private walker state for committed-wire coherence, which confirms the seam is real.
17. `quicksilver/fiat_shamir.py` rejects zero transcript challenges through SHA-256 rejection sampling and binds the circuit into the transcript, giving a local pattern for zero-challenge guard behavior.
18. `quicksilver/lpn_vole.py` states its defaults are not secure and base OT/SPCOT is not implemented, while `README.md` and `demos/lpn_vole_demo.py` present `LpnParams.default(...)` as the ergonomic path.
19. `quicksilver/einsum.py` materializes contractions explicitly and documents no optimization passes. This is fine for pedagogical tests but should be paired with cost limits before user-controlled large tensor shapes are exposed.
20. `quicksilver/zk_reachability.py` documents roughly `n^2 * k` multiplication-gate scaling; the demos validate small cases, but no CI-enforced benchmark or resource ceiling exists.
21. `demos/lpn_vole_demo.py` includes a scaling loop over `(32, 128, 512, 2048)` output VOLE lengths. The `2048` row took about 20.4 seconds locally, so it is a full-validation candidate, not a fast smoke candidate.
22. `../../2026-05-07-implementation-followups/tensor-quicksilver-validation-runner/Makefile` already defines `PYTHON ?= python3`, `test`, `quick-validate`, and `validate` targets. That branch should be reviewed or cherry-picked before creating duplicate validation-runner work.
23. `../../2026-05-07-implementation-followups/tensor-quicksilver-validation-runner/pyproject.toml` already declares `requires-python = ">=3.10"` and `pytest>=8` under `dev` and `test` extras.
24. `../../2026-05-07-implementation-followups/tensor-quicksilver-validation-runner/tests/test_package.py` locks the current narrow top-level `quicksilver.__all__` export surface.

## Known blockers and constraints

- No blocker for producing this audit report.
- External pushes, PR creation, tracker updates, deploys, and merges are out of scope.
- This branch has no local packaging metadata or CI configuration.
- The README's literal `python ...` validation commands fail in this worker because `python` is absent.
- `pytest` is installed globally for `python3` here, but the repo does not declare it.
- `.pytest_cache/` is an ignored byproduct of validation; default `git status --short` hides it.
- Local commits may be blocked in these worktrees if Git needs to write index locks outside the writable root, as previous tensor reports observed. This item does not require a commit.
- Product/security decisions are needed before changing crypto-facing public APIs, LPN default naming, top-level exports, or whether the repo becomes an installable package.

## Queue-readiness assessment

Ready for separate implementation issues:

- Zero-challenge guard across prime, boolean, and polynomial batched APIs.
- Message/share shape validation.
- Boolean witness strictness.
- README and security-boundary corrections.
- Validation-runner/packaging promotion from the existing follow-up branch.

Not ready without human product judgment:

- Expanding `quicksilver.__all__` beyond prime-field basics.
- Choosing `>=3.10` versus `>=3.11` as a supported Python floor.
- Deciding whether `demos/transitive_closure.py` should be restored locally, linked as sibling `tensor-logic`, or removed as a local claim.
- Deciding whether LPN demo defaults should be renamed, gated with an explicit `security_level="demo"`, or left as-is with stronger docs.
- Deciding whether polynomial committed-wire access should become a public trace object or remain an internal/testing seam.

## Five safe implementation tasks

### 1. Reject zero verifier challenges in all public batched APIs

Owned files:

- `quicksilver/protocol.py`
- `quicksilver/boolean.py`
- `quicksilver/polynomial.py`
- `tests/test_quicksilver.py`
- `tests/test_boolean.py`
- `tests/test_lpn_vole.py`

Acceptance criteria:

- `protocol.verify(...)` rejects `chi == 0` with a documented behavior.
- `boolean.verify(...)` applies the same zero-challenge policy.
- `prove_polys(...)` and `verify_polys(...)` reject `chi == 0`.
- Regression tests prove malicious prime and boolean transcripts no longer accept when `chi == 0`.
- Existing `run(...)`, Fiat-Shamir, LPN integration, and normal tamper tests remain green.

Smallest useful validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py tests/test_lpn_vole.py tests/test_fiat_shamir.py -q -p no:cacheprovider`

### 2. Harden message and share shape validation

Owned files:

- `quicksilver/protocol.py`
- `quicksilver/boolean.py`
- `tests/test_quicksilver.py`
- `tests/test_boolean.py`
- `tests/test_fiat_shamir.py`

Acceptance criteria:

- Prime verifier checks exact `CommitMessage.d_values` count `num_inputs + num_muls`.
- Boolean verifier checks exact `BCommitMessage.d_values` count `num_inputs + num_ands`.
- Prime and boolean verifiers check exact assertion-opening counts and verifier share length `circuit.vole_count()`.
- Short messages/shares fail through the chosen public behavior instead of leaking `StopIteration`.
- Extra message/share elements are rejected rather than silently ignored.

Smallest useful validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py tests/test_fiat_shamir.py -q -p no:cacheprovider`

### 3. Promote the existing validation-runner follow-up

Owned files:

- `pyproject.toml`
- `Makefile`
- `_quicksilver_build_backend.py`
- `tests/test_package.py`
- `README.md`

Starting point:

- Review or cherry-pick `../../2026-05-07-implementation-followups/tensor-quicksilver-validation-runner` commit `c45b603`.

Acceptance criteria:

- Repo declares package metadata, a supported Python floor, empty runtime dependencies, and `pytest` test/dev extras.
- Fast validation uses `python3` by default and is executable through a stable command such as `make quick-validate`.
- Package import/export test covers the intentional `quicksilver.__all__` surface.
- README commands no longer fail in this worker because `python` is missing.
- Runtime package remains third-party-free.

Smallest useful validation:

- `python3 -m pytest tests/ -q`
- `make quick-validate`
- `python3 -m pip install -e ".[test]"` in a disposable environment if dependency installation is allowed.

### 4. Reconcile README claims and cryptography boundary language

Owned files:

- `README.md`
- Optional: `docs/security-boundary.md`

Acceptance criteria:

- README no longer claims eight modules or six demos unless the file inventory actually matches.
- README uses `python3` or points at a repo-managed validation command.
- Missing local `demos/transitive_closure.py` reference is removed, qualified as sibling `tensor-logic`, or backed by a local file.
- Trusted-dealer setup, insecure demo LPN defaults, designated-verifier Fiat-Shamir, no public verification, pure-Python performance, and no production parameter table are visible near usage examples.
- "Real-cryptography demos" wording is narrowed or clearly framed as pedagogical/demo-only.

Smallest useful validation:

- `rg -n "Eight modules|six runnable|demos/transitive_closure.py|python -m pytest|Real-cryptography" README.md`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider`
- Run any demo whose README command text changes.

### 5. Make boolean witness handling strict

Owned files:

- `quicksilver/boolean.py`
- `tests/test_boolean.py`
- Optional: `README.md` if witness semantics are documented.

Acceptance criteria:

- Boolean prover rejects witness values outside `{0, 1}` with a clear `ValueError`, or docs explicitly state and tests lock down low-bit coercion if that behavior is intentional.
- Tests cover `run(c, [2])`, `run(c, [-1])`, and another non-bit value that currently passes through low-bit masking.
- Existing boolean completeness, wrong-witness, and tamper tests remain green.

Smallest useful validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_boolean.py -q -p no:cacheprovider`

## Suggested queue order

1. Reject zero verifier challenges. It has the clearest soundness impact and prior reproduction evidence.
2. Harden message/share shape validation. It touches the same public verifier boundary and should be reviewed nearby.
3. Promote validation-runner packaging work from commit `c45b603`. Avoid duplicate metadata work.
4. Reconcile README and security-boundary language. This can follow or accompany validation-runner README edits.
5. Make boolean witness handling strict. It is isolated and low-risk once the larger verifier boundary changes are queued.

## Final handoff

- Product code changed: none.
- Report written: `docs/overnight/2026-05-07-30min-extension-b/tensor-quicksilver-zk-validation-queue-plan.md`.
- Commit created: none; HEAD remains `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.
- PR URL: none; PR creation was out of scope.
- Required validation command: `git status --short`.
- Required validation result: passed, exit 0, output `?? docs/`.
- Exact untracked file check: `git status --short --untracked-files=all` reported `?? docs/overnight/2026-05-07-30min-extension-b/tensor-quicksilver-zk-validation-queue-plan.md`.
- Blockers: none for this audit. Implementation tasks need separate code branches and, for packaging/API choices, product-owner review.
