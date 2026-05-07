# tensor-quicksilver-zk 30-minute extension action plan

Queue item: `tensor-quicksilver-zk-30min-action-plan`  
Branch: `codex/goal-tensor-quicksilver-zk-30min-action-plan`  
Repo path: `/Users/jwalinshah/projects/agent-stack/.agent-stack-worktrees/2026-05-07-30min-extension/tensor-quicksilver-zk-30min-action-plan`  
HEAD: `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`  
Remote: `origin https://github.com/jwalin-shah/quicksilver-zk.git`

## Scope

This pass was read-only planning/synthesis except for this report. I did not
edit product code, generated assets, external services, trackers, remotes, or
PRs. The work consolidates current repo evidence plus prior overnight reports
into implementation-ready queue items.

Changed file:

- `docs/overnight/2026-05-07-30min-extension/tensor-quicksilver-zk-action-plan.md`

## Prior overnight reconciliation

This worktree did not contain a pre-existing `docs/overnight/` directory before
this report. Sibling overnight worktrees did contain six repo-specific reports,
all from HEAD `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.

| Prior report | Already covered | Still missing | Move into implementation queue |
| --- | --- | --- | --- |
| `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-architecture-map/docs/overnight/tensor-quicksilver-zk-architecture-map.md` | Module boundaries, import direction, weak polynomial committed-wire seam, boolean/protocol duplication, witness-layout coupling, implicit shape validation. | No executable issue ordering; did not choose top security fix versus packaging/docs work. | Message/share shape validation; explicit committed-wire interface can wait behind security/API hardening. |
| `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-validation-map/docs/overnight/tensor-quicksilver-zk-validation-map.md` | Current test/demo health, missing packaging/CI/lint, `python` command failure, slow LPN demo, stale README counts. | Did not notice the later implementation-followup branch that already adds packaging and validation runner files. | Promote or review the existing validation-runner branch before reimplementing metadata. |
| `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-risk-register/docs/overnight/tensor-quicksilver-zk-risk-register.md` | Highest-severity issue: direct `verify(..., chi=0, ...)` accepts malicious prime and boolean transcripts; also insecure LPN defaults, trusted-dealer boundary, shape validation, boolean witness truncation. | The zero-challenge fix has not landed in this worktree. | First implementation issue should reject zero challenges across prime, boolean, and polynomial verification paths. |
| `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-docs-claims/docs/overnight/tensor-quicksilver-zk-docs-claims.md` | README claims audit: 76 tests true; five demos, not six; 12 implementation modules excluding `__init__`, not eight; missing local `demos/transitive_closure.py`; `python3` works while `python` does not. | Docs fixes were not applied; README still carries stale onboarding commands and inventory in this worktree. | README/docs correction should follow packaging/security fixes or land with them if low-risk. |
| `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-dependency-surface/docs/overnight/tensor-quicksilver-zk-dependency-surface.md` | Runtime is stdlib-only; tests require undeclared `pytest`; no package metadata, CI, Makefile, Dockerfile, or lockfile; Python syntax floor is 3.10+. | No final decision on supported Python version or whether repo should be installable. | Validation metadata issue should state `>=3.10` unless owner chooses stricter alignment with sibling `tensor-logic` `>=3.11`. |
| `../../2026-05-07-overnight-marathon/tensor-quicksilver-zk-workflow-handoff/docs/overnight/tensor-quicksilver-zk-workflow-handoff.md` | Handoff gaps: no canonical setup, no public API export decision, no license, slow demo split, sibling tensor-logic bridge ambiguity. | It intentionally stopped at audit. | Keep API export/license decisions as human-product questions unless directly needed by packaging tests. |

Additional reconciliation: `../../2026-05-07-implementation-followups/tensor-quicksilver-validation-runner/`
contains a clean follow-up branch `codex/goal-tensor-quicksilver-validation-runner`
at commit `c45b603` that already adds `pyproject.toml`, `Makefile`,
`_quicksilver_build_backend.py`, `tests/test_package.py`, and README command
updates. That branch addresses much of the packaging/validation-runner queue
item but is not present in this worktree.

## Current validation evidence

| Command | Result |
| --- | --- |
| `git branch --show-current` | `codex/goal-tensor-quicksilver-zk-30min-action-plan`. |
| `git rev-parse HEAD` | `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`. |
| `git status --short` before this report | Empty output. |
| `git status --short` after this report | Passed, exit 0, output `?? docs/`. |
| `git status --short --untracked-files=all` after this report | Passed, exit 0, output `?? docs/overnight/2026-05-07-30min-extension/tensor-quicksilver-zk-action-plan.md`. |
| `rtk pytest tests/ -v` | Passed: `76 passed`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider` | Passed: `76 passed in 0.49s`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest --collect-only -q tests/ -p no:cacheprovider` | Passed: `76 tests collected in 0.11s`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 demos/quicksilver_demo.py` | Passed; prime-field and polynomial demos accepted. |
| `PYTHONDONTWRITEBYTECODE=1 python3 demos/zk_einsum.py` | Passed; matmul, grandparent, and one-step closure demos accepted. |
| `PYTHONDONTWRITEBYTECODE=1 python3 demos/quicksilver_boolean_demo.py` | Passed; 10-bit scaling row ran in about 249 ms. |
| `PYTHONDONTWRITEBYTECODE=1 python3 demos/zk_graph_reachability.py` | Passed; largest printed scaling row was `n=16`, `muls=1408`, about 20.7 ms. |
| `PYTHONDONTWRITEBYTECODE=1 python3 demos/lpn_vole_demo.py` | Passed; slowest row `n_out=2048`, `k_base=4096`, about 20.5 s. |
| `python -m pytest --version` | Failed with `python: command not found`; README still uses the stale `python` spelling. |

The default required queue validation remains `git status --short`. After this
report, it should show only the new report path under `docs/overnight/`.

## Concrete file observations

1. `README.md:10-14` still claims about 2,500 lines, eight modules, 76 tests,
   and six runnable demos. Local inventory supports 76 tests, but there are
   12 implementation modules excluding `__init__.py` and five demo files.
2. `README.md:167-178` documents `python -m pytest` and `python demos/...`
   commands. This shell has no `python` executable; all successful validation
   used `python3`.
3. `README.md:183-199` references `demos/transitive_closure.py` as local context
   for tensor-logic reachability. `rg --files` shows no such file in this repo;
   prior reports found it in sibling `tensor-logic`.
4. `quicksilver/circuit.py:115-117` defines the core VOLE cost contract as
   `num_inputs + num_muls + 1`; this is the right anchor for validation-runner
   and shape-check tests.
5. `quicksilver/protocol.py:251-263` exposes `verify(..., chi, ...)` without a
   nonzero challenge guard. `protocol.run` uses `field.rand_nonzero()` at
   `quicksilver/protocol.py:266-272`, so safe helper usage does not cover direct
   verifier API misuse.
6. `quicksilver/boolean.py:373-389` has the same caller-supplied `chi` verifier
   shape as the prime protocol, while `quicksilver/boolean.py:390-397` samples a
   nonzero challenge only in the end-to-end helper.
7. `quicksilver/polynomial.py:126-147` and `quicksilver/polynomial.py:170-186`
   validate polynomial degree and mask lengths, but do not reject `chi == 0` in
   the batched polynomial API.
8. `quicksilver/boolean.py:231-239` silently coerces witness inputs with
   `int(next(wit)) & 1`; constants are stricter at
   `quicksilver/boolean.py:143-158`, so witness handling can hide caller bugs.
9. `quicksilver/lpn_vole.py:43-46` states default LPN parameters are not secure,
   while `quicksilver/lpn_vole.py:68-72` exposes them through the ergonomic
   `LpnParams.default(...)` constructor used by README examples.
10. `quicksilver/fiat_shamir.py:96-112` already rejects zero transcript
    challenges during SHA-256 rejection sampling, which gives an implementation
    pattern for direct verifier API hardening.
11. `tests/test_quicksilver.py:166-209` hand-crafts a malicious prime-field
    multiplication transcript, but it uses `F.rand_nonzero()` and does not
    assert rejection at `chi == 0`.
12. `tests/test_boolean.py:144-153` covers boolean batched-check tampering with
    `GF128.rand_nonzero()`, but does not cover zero-challenge rejection or
    non-bit witness rejection.
13. `tests/test_lpn_vole.py:77-120` proves LPN-extended VOLE plugs into the
    protocol and preserves tamper rejection under nonzero challenge; it does not
    harden parameter naming or challenge guards.
14. `tests/test_einsum.py:160-179` proves the grandparent-rule einsum locally,
    giving a good self-contained replacement for README wording that currently
    points at missing `transitive_closure.py`.
15. `tests/test_zk_reachability.py:123-134` only checks monotonic circuit-size
    growth; it does not expose a public cost-estimation helper for callers who
    might build oversized circuits.
16. `quicksilver/__init__.py:12-17` exports only prime-field basics. README
    examples already import boolean, LPN, Fiat-Shamir, einsum, and reachability
    from submodules, so top-level API expansion should be a deliberate decision,
    not a side effect of packaging.

## Known blockers and constraints

- No blocker for this report or local validation.
- External pushes, PR creation, tracker updates, and merges are out of scope for
  this Goal Pack item.
- The current worktree lacks packaging metadata; `python3` works only because
  commands run from the repo root and tests/demos mutate `sys.path`.
- The default `python` command is unavailable in this environment.
- `.pytest_cache/` exists as an ignored artifact after validation; default
  `git status --short` does not report it.
- Security and product posture are intentionally pedagogical. Work that changes
  the public cryptographic API should be implemented as separate, reviewed code
  issues with focused regression tests.

## Implementation-ready follow-up tasks

### 1. Reject zero verifier challenges in all public batched APIs

Owned files:

- `quicksilver/protocol.py`
- `quicksilver/boolean.py`
- `quicksilver/polynomial.py`
- `tests/test_quicksilver.py`
- `tests/test_boolean.py`
- `tests/test_lpn_vole.py`

Acceptance criteria:

- `protocol.verify(...)` returns `False` or raises a documented `ValueError`
  when `chi == 0`; choose one behavior and test it.
- `boolean.verify(...)` applies the same zero-challenge policy.
- `prove_polys(...)` and `verify_polys(...)` reject `chi == 0`.
- Regression tests simulate the malicious prime and boolean transcripts from
  the risk-register report and prove they no longer accept at `chi == 0`.
- Existing `run(...)`, `run_ni(...)`, LPN, and normal tamper tests remain green.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py tests/test_lpn_vole.py tests/test_fiat_shamir.py -q -p no:cacheprovider`

### 2. Harden message and share shape validation

Owned files:

- `quicksilver/protocol.py`
- `quicksilver/boolean.py`
- `tests/test_quicksilver.py`
- `tests/test_boolean.py`
- `tests/test_fiat_shamir.py`

Acceptance criteria:

- Prime verifier checks exact `CommitMessage.d_values` count
  `num_inputs + num_muls`, exact assertion-opening count, and exact verifier
  share length `circuit.vole_count()`.
- Boolean verifier checks exact `BCommitMessage.d_values` count
  `num_inputs + num_ands`, exact assertion-opening count, and exact verifier
  share length `circuit.vole_count()`.
- Short messages/shares fail with a clear documented behavior instead of
  leaking `StopIteration`.
- Extra message/share elements are rejected, not silently ignored.
- Fiat-Shamir tests still pass and transcript binding remains unchanged.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py tests/test_fiat_shamir.py -q -p no:cacheprovider`

### 3. Promote the validation-runner follow-up instead of reimplementing it

Owned files:

- `pyproject.toml`
- `Makefile`
- `_quicksilver_build_backend.py`
- `tests/test_package.py`
- `README.md`

Starting point:

- Review or cherry-pick `../../2026-05-07-implementation-followups/tensor-quicksilver-validation-runner`
  commit `c45b603`.

Acceptance criteria:

- Repo declares package metadata, `requires-python`, empty runtime
  dependencies, and `pytest` test/dev extras.
- `Makefile` or equivalent defines a fast validation command using `python3`.
- Package import/export test covers the intentional `quicksilver.__all__`
  surface.
- README validation commands no longer fail in this environment due to
  `python` missing.
- Runtime package remains third-party-free.

Validation:

- `python3 -m pytest tests/ -q`
- `make quick-validate`
- `python3 -m pip install -e ".[test]"` in a disposable environment when
  dependency installation is allowed.

### 4. Reconcile README claims and cryptography boundary language

Owned files:

- `README.md`
- Optional: `docs/security-boundary.md`

Acceptance criteria:

- README stops claiming eight modules and six demos, or updates the counts to
  match `rg --files quicksilver tests demos`.
- README uses `python3` or a repo-managed validation command.
- Missing local `demos/transitive_closure.py` reference is removed, converted to
  an inline recurrence snippet, or explicitly labeled as sibling `tensor-logic`
  context.
- Trusted-dealer setup, insecure demo LPN defaults, designated-verifier
  Fiat-Shamir, no public verification, pure-Python performance, and no
  production parameter table are visible near usage examples.
- "Real-cryptography demos" wording is narrowed or clearly marked
  pedagogical/demo-only.

Validation:

- `rg -n "Eight modules|six runnable|demos/transitive_closure.py|python -m pytest|Real-cryptography" README.md`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider`
- Run any demo whose README command text changes.

### 5. Make boolean witness handling strict

Owned files:

- `quicksilver/boolean.py`
- `tests/test_boolean.py`
- Optional: `README.md` if witness semantics are documented.

Acceptance criteria:

- Boolean prover rejects witness values outside `{0, 1}` with a clear
  `ValueError`.
- Tests cover `run(c, [2])`, `run(c, [-1])`, and another non-bit value that
  currently passes through low-bit masking.
- Existing boolean completeness, wrong-witness, and tamper tests remain green.
- If low-bit coercion is intentionally preserved instead, README/API docs state
  that behavior explicitly and tests lock it down.

Validation:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_boolean.py -q -p no:cacheprovider`

## Suggested queue order

1. Reject zero verifier challenges. This is the clearest security/soundness
   footgun and has direct regression evidence from prior audit work.
2. Harden message/share shape validation. This is the same public API boundary
   and should be reviewed close to the zero-challenge change.
3. Promote validation-runner packaging work from commit `c45b603`. Avoid
   duplicating already-implemented metadata work.
4. Reconcile README and security-boundary language. This should land after or
   with validation-runner README edits.
5. Make boolean witness handling strict. Small, isolated API hardening after the
   main verifier boundary work.

## Final handoff

- Product code changed: none.
- Report written: `docs/overnight/2026-05-07-30min-extension/tensor-quicksilver-zk-action-plan.md`.
- Commit created: none; HEAD remains `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.
- PR URL: none; PR creation was out of scope.
- Required validation command: `git status --short` passed, exit 0, output
  `?? docs/`.
- Exact untracked file check: `git status --short --untracked-files=all`
  reported `?? docs/overnight/2026-05-07-30min-extension/tensor-quicksilver-zk-action-plan.md`.
- Blockers: none for this audit. Future implementation tasks should be separate
  code changes with the validation commands listed above.
