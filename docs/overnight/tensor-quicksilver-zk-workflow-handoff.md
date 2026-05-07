# tensor-quicksilver-zk workflow-handoff audit

Queue item: `tensor-quicksilver-zk-workflow-handoff`
Repo path: `/Users/jwalinshah/projects/agent-stack/.agent-stack-worktrees/2026-05-07-overnight-marathon/tensor-quicksilver-zk-workflow-handoff`
Branch: `codex/goal-tensor-quicksilver-zk-workflow-handoff`
HEAD at audit time: `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`
Remote: `origin https://github.com/jwalin-shah/quicksilver-zk.git`
Scope: read-only audit plus this report. No product code, generated data, external services, pushes, tracker updates, or PR creation.

## Repo purpose and current state

`tensor-quicksilver-zk` is a small pedagogical Python implementation of the QuickSilver zero-knowledge proof protocol. The core package implements prime-field VOLE/IT-MAC commitments, arithmetic-circuit proving, a polynomial-extension check, a boolean `GF(2^128)` instantiation, a Fiat-Shamir designated-verifier variant, an LPN-style VOLE extension demo, and tensor-logic frontends for einsum and graph reachability.

Initial state was clean: `git status --short --branch` printed only `## codex/goal-tensor-quicksilver-zk-workflow-handoff`. `git log --oneline -5` shows a single commit, `60b7fbe Initial commit: QuickSilver ZK proof system`.

The repo has no project metadata discovered by `rg --files -g 'pyproject.toml' -g 'setup.py' -g 'setup.cfg' -g 'requirements*.txt' -g 'uv.lock' -g 'Makefile' -g 'justfile' -g '.github/**'`; command exited 1 with no matches. The only top-level files before this report were `.gitignore`, `README.md`, `quicksilver/`, `tests/`, and `demos/`.

## Concrete evidence

- `llm-tldr tree .` found three code-bearing directories: `quicksilver/`, `tests/`, and `demos/`; no existing `docs/` directory existed before this report.
- `git ls-files` lists 27 tracked files: `.gitignore`, `README.md`, five demo scripts, thirteen `quicksilver/*.py` files, and seven test files.
- `wc -l README.md quicksilver/*.py tests/*.py demos/*.py` reported 4,259 total lines: 1,879 lines under `quicksilver/`, 1,130 under `tests/`, 738 under `demos/`, and 212 in `README.md`.
- `README.md` claims "About 2,500 lines", "Eight modules", "76 tests", and "six runnable demos"; local inventory shows 4,259 total lines, thirteen package modules, 76 collected tests, and five demo files.
- `README.md` and `quicksilver/zk_reachability.py` reference `demos/transitive_closure.py`; that file is not in this repo. It exists in sibling tensor repos found through `/Users/jwalinshah/projects/agent-stack/repos.json`.
- `quicksilver/__init__.py` exports only `F`, `Fp`, `Wire`, `Circuit`, `prove`, `verify`, and `run`; boolean, LPN, polynomial, Fiat-Shamir, einsum, and reachability APIs require submodule imports.
- `quicksilver/circuit.py` defines the arithmetic DSL and `vole_count() = num_inputs + num_muls + 1`, making VOLE consumption easy for next workers to validate.
- `quicksilver/protocol.py` owns the prime-field interactive protocol through `_ProverWalker`, `_VerifierWalker`, `prove`, `verify`, and `run`; the public helper samples `chi` with `field.rand_nonzero()`.
- `quicksilver/vole.py` is explicit that VOLE setup is simulated by a trusted dealer. `quicksilver/lpn_vole.py` adds extension mechanics but still generates the sparse base correlation centrally.
- `quicksilver/lpn_vole.py` states its defaults `(k=2N, t=N//4)` are not secure and are demonstration parameters only.
- `quicksilver/gf2k.py` sets `p = 2**128` for interface compatibility while warning it is not a prime; anything using `field.p` generically needs care.
- `quicksilver/fiat_shamir.py` makes proofs non-interactive but still designated-verifier, because verification needs the secret `Delta`.
- `quicksilver/einsum.py` materialises contractions directly and documents that it has no optimisation passes. `quicksilver/zk_reachability.py` builds on the same tensor-logic premise.
- `tests/test_quicksilver.py`, `tests/test_boolean.py`, `tests/test_einsum.py`, `tests/test_fiat_shamir.py`, `tests/test_lpn_vole.py`, and `tests/test_zk_reachability.py` cover completeness, tampering/soundness checks, parser/dim validation, Fiat-Shamir binding, LPN correlation, and reachability witness assembly.
- `python -m pytest tests/ -q -p no:cacheprovider` failed in this shell with `/opt/homebrew/bin/bash: line 1: python: command not found`.
- `python3 -m pytest tests/ -q -p no:cacheprovider` passed: `76 passed in 0.45s`.
- All five demo scripts passed under `python3`. `demos/lpn_vole_demo.py` is materially slower than the others because its scaling section took about 20.3s for `n_out=2048`.
- `.gitignore` only ignores `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`, and `*.egg-info/`; there are no repository-specific generated-artifact rules beyond Python basics.

## Workflow-handoff risks and stale assumptions

1. README/runtime command drift. The README's test command uses `python`, but this local worker shell only has `python3`. A new worker following the README literally fails before collecting tests.
2. README inventory drift. The README claims eight modules and six demos, but tracked files show thirteen package modules and five demos. It also references an absent `demos/transitive_closure.py`.
3. Packaging gap. There is no `pyproject.toml`, requirements file, lockfile, CI config, lint config, or Makefile. Tests work only because execution starts from repo root and the tests mutate `sys.path`.
4. Cryptography boundary can be misread. The repo is pedagogical, but labels such as "Real-cryptography demos" sit near code that still uses a trusted dealer, non-secure LPN defaults, and designated-verifier proofs. That is fine for a demo repo, but unsafe as a product handoff without sharper disclaimers.
5. Public API boundary is narrow. `quicksilver/__init__.py` exposes only the prime-field protocol; the README demonstrates several submodule imports. A future agent could accidentally widen API surface or duplicate wrapper helpers without an explicit export decision.
6. Demo validation cost is uneven. Most demos run in milliseconds, but `demos/lpn_vole_demo.py` took over 20 seconds locally because it includes a large scaling point. A "run all demos" validation step should either tolerate that or split fast and slow modes.
7. Tensor-logic ownership is split. This repo contains `quicksilver/einsum.py` and reachability proofs, while the clearer tensor-logic demos live in sibling repos. Sibling `tensor-logic` currently has a dirty worktree, so bridge work needs a deliberate cross-repo contract rather than ad hoc imports.
8. No supported Python version is declared. The observed passing interpreter is Python 3.12.8, but the repo does not state whether 3.10/3.11/3.13 are supported.
9. Randomized tests pass today but are not seeded across the suite. Tests use random field elements in several places; failures are unlikely but reproduction would be easier with optional deterministic seeds for property-style checks.
10. License/reuse status is unclear from this worktree. There is no local `LICENSE`, so reuse, publication, and package distribution need owner confirmation before release work.

## Sibling-repo overlap

`repos.json` places this repo in the `tensor` group alongside `tensor-experiments`, `tensor-fafsa-engine`, `tensor-taxes`, and `tensor-logic`.

The closest overlap is `tensor-logic` and `tensor-experiments`. Read-only search found `demos/transitive_closure.py`, `demos/train_kg.py`, `tensor_logic/rules.py`, and `tensor_logic/language.py` using the same einsum-as-rule framing. `tensor-logic` also has `pyproject.toml` and a broader validation command (`python3 -m pytest -q` in `repos.json`), unlike this repo.

Handoff risk: this repo's README explains its premise by pointing at sibling demos, but there is no dependency, copy, contract test, or doc link that tells a worker which repo owns the canonical tensor-logic examples. Any integration task should start by deciding whether this repo stays self-contained or grows an explicit sibling bridge.

`tensor-fafsa-engine` and `tensor-taxes` appear to be domain knowledge-base apps with `pyproject.toml` and tests. They are useful as examples of packaging/validation hygiene in the tensor group, but they do not share direct QuickSilver/einsum code based on the shallow file inventory.

## Next independently grabbable tasks

### 1. Normalize packaging and validation entrypoints

Scope: add minimal project metadata and documented commands without changing protocol behavior.

Suggested files: `pyproject.toml`, `README.md`, maybe `.github/workflows/tests.yml` if CI is in scope.

Acceptance criteria:
- `python3 -m pytest tests/ -q -p no:cacheprovider` remains green.
- A fresh worker can install/test from documented commands without manually editing `PYTHONPATH`.
- README no longer assumes `python` exists when this repo's observed command is `python3`.
- If dependency metadata is added, `pytest` is declared as a test dependency.

Validation candidates:
- `python3 -m pytest tests/ -q -p no:cacheprovider` expected pass.
- `python3 -m pytest --collect-only -q -p no:cacheprovider tests/` expected 76 collected until tests change.
- `git status --short` expected to show only intentional metadata/docs changes.

### 2. Reconcile README claims and demo inventory

Scope: docs-only correction of stale repo claims and demo commands.

Suggested files: `README.md`; optionally add a small `docs/demos.md` if the README should stay short.

Acceptance criteria:
- README counts match `rg --files quicksilver tests demos` and `wc -l` within a stated convention.
- Demo count is five unless a sixth demo is added intentionally.
- The `transitive_closure.py` reference says it lives in sibling tensor repos or is removed from this repo's local layout section.
- The LPN demo is marked as slower than the other demos, or the command list splits fast/slow demos.

Validation candidates:
- `rg --files demos` expected five files unless the task deliberately adds one.
- `python3 demos/quicksilver_demo.py` expected pass.
- `python3 demos/quicksilver_boolean_demo.py` expected pass.
- `python3 demos/zk_einsum.py` expected pass.
- `python3 demos/zk_graph_reachability.py` expected pass.
- `python3 demos/lpn_vole_demo.py` expected pass but slow, about 20s locally because of `n_out=2048`.

### 3. Clarify public API exports and examples

Scope: decide which APIs should be top-level versus submodule-only, then make examples/tests enforce that decision.

Suggested files: `quicksilver/__init__.py`, `tests/test_quicksilver.py`, `tests/test_boolean.py`, `tests/test_einsum.py`, `tests/test_fiat_shamir.py`, `README.md`.

Acceptance criteria:
- Top-level exports are documented and tested.
- Boolean, Fiat-Shamir, LPN, polynomial, einsum, and reachability APIs either remain explicitly submodule-only or are intentionally exported.
- README examples use the chosen import style consistently.
- No protocol logic changes are made unless an import/export test requires a trivial wrapper.

Validation candidates:
- `python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py tests/test_einsum.py tests/test_fiat_shamir.py -q -p no:cacheprovider` expected pass.
- `python3 -m pytest tests/ -q -p no:cacheprovider` expected pass.

### 4. Add a security boundary note

Scope: docs-only security/readiness clarification for cryptographic claims.

Suggested files: `README.md`, optionally `SECURITY.md` or `docs/security-boundary.md`.

Acceptance criteria:
- The trusted-dealer status of `quicksilver/vole.py` is explicit near the first usage example.
- `quicksilver/lpn_vole.py` defaults are described as demonstration-only, not concrete security parameters.
- Fiat-Shamir is described as designated-verifier, not public-verifier.
- "Real-cryptography demos" wording is either narrowed or clearly framed as pedagogical.

Validation candidates:
- `python3 -m pytest tests/ -q -p no:cacheprovider` expected pass if docs-only.
- `python3 demos/lpn_vole_demo.py` expected pass if the task touches LPN demo text.

### 5. Define the tensor-logic bridge contract

Scope: make the relationship between this repo and sibling tensor-logic repos explicit without taking a dependency by accident.

Suggested files: `README.md`, `docs/tensor-logic-bridge.md`, `tests/test_einsum.py`, `tests/test_zk_reachability.py`.

Acceptance criteria:
- The doc names which sibling repo owns `transitive_closure.py` and `train_kg.py`.
- This repo states whether its `quicksilver/einsum.py` is a self-contained compiler or a compatibility target for `tensor_logic`.
- At least one local test demonstrates the bridge claim using only local code, or the task explicitly records why cross-repo tests are out of scope.
- No sibling repo files are modified from this worktree.

Validation candidates:
- `python3 -m pytest tests/test_einsum.py tests/test_zk_reachability.py -q -p no:cacheprovider` expected pass.
- Optional read-only sibling check: `llm-tldr search "transitive_closure|einsum" /Users/jwalinshah/projects/tensor/tensor-logic`.

## Validation command candidates and observed status

Required queue validation:
- `git status --short` should exit 0. After this report, expected output is the uncommitted `docs/` report path.

Observed working validation:
- `python3 -m pytest tests/ -q -p no:cacheprovider` passed: `76 passed in 0.45s`.
- `python3 -m pytest --collect-only -q -p no:cacheprovider tests/` passed: `76 tests collected in 0.11s`.
- `python3 demos/quicksilver_demo.py` passed.
- `python3 demos/quicksilver_boolean_demo.py` passed.
- `python3 demos/lpn_vole_demo.py` passed, with the largest scaling row `n_out=2048` taking about `20258.3 ms`.
- `python3 demos/zk_einsum.py` passed.
- `python3 demos/zk_graph_reachability.py` passed.

Observed broken/stale validation:
- `python -m pytest tests/ -q -p no:cacheprovider` failed locally because `python` is not installed or not on PATH in this shell.

Missing validation surfaces:
- No lint command found.
- No type-check command found.
- No build/package command found.
- No CI workflow found.

## Decisions made during this audit

- Use `python3` for local execution evidence because `python` fails in this shell.
- Treat sibling tensor repos as read-only evidence only. The `tensor-logic` sibling has dirty state, and this queue item is scoped to this repo/worktree.
- Do not create a PR or commit; the goal pack asks for one report in the worktree and forbids external mutation.
- Avoid editing README or code even where stale claims were obvious, because the queue item is an audit handoff, not implementation.

## Non-goals

- No cryptographic proof review against the QuickSilver paper.
- No production hardening, parameter selection, or replacement of trusted setup.
- No package publishing or dependency installation.
- No CI setup.
- No product-code changes.
- No sibling-repo edits.
- No external tracker updates.
- No PR creation.

## Unknowns for morning review

- Should this repo remain a self-contained pedagogical demo, or should it become an installable package?
- Which Python versions should be supported?
- Should top-level imports expose the boolean, Fiat-Shamir, LPN, polynomial, einsum, and reachability APIs?
- Should the tensor-logic bridge point to `tensor-logic`, `tensor-experiments`, or copy a local minimal `transitive_closure.py` demo?
- Is there an intended license for this repo?
- Should LPN scaling remain in the default demo, or should slow scaling be opt-in?
- Should future agents open Linear issues for the tasks above, or keep these as local Work Packs until the repo direction is chosen?

