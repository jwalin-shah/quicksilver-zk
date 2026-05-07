# tensor-quicksilver-zk risk-register audit

Queue item: `tensor-quicksilver-zk-risk-register`
Date: 2026-05-07
Branch: `codex/goal-tensor-quicksilver-zk-risk-register`
Repo path: `/Users/jwalinshah/projects/agent-stack/.agent-stack-worktrees/2026-05-07-overnight-marathon/tensor-quicksilver-zk-risk-register`
Focus area: security, credentials, data, deployment, destructive-command, and external-service risks.

## Executive summary

`tensor-quicksilver-zk` is a compact educational Python implementation of a QuickSilver-style designated-verifier ZK proof system. It contains local protocol code, tests, and demos only: no package metadata, CI workflow, deployment config, network client, credential loader, or external service integration was present in the worktree.

The most important finding is an API-level soundness footgun: the public interactive verifiers accept a caller-supplied `chi` challenge and do not reject `chi == 0`. The built-in `run(...)` helpers use `rand_nonzero()`, and Fiat-Shamir `Transcript.challenge()` rejects zero, but direct users of `verify(...)` can accidentally disable the multiplication/AND checks by passing zero. I reproduced this locally for both the prime-field and boolean verifiers with malicious transcripts: zero challenge returned `True`, while a fresh nonzero challenge returned `False`.

The next tier of risk is expectation management. The docs correctly say this is educational, uses a trusted dealer, and has insecure LPN defaults, but the public APIs and README snippets make those modes easy to use as if they were deployable cryptography. This is especially relevant because the README also has stale inventory claims: it says six demos and references `demos/transitive_closure.py`, while the repo has five demo files and no such file.

## Current state

- `git status --short --branch` reported only `## codex/goal-tensor-quicksilver-zk-risk-register`; no dirty files before the audit.
- `git rev-parse HEAD` returned `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.
- `git remote -v` shows `origin https://github.com/jwalin-shah/quicksilver-zk.git` for fetch and push.
- `rg --files` found `README.md`, 13 package files under `quicksilver/`, 7 test files under `tests/`, and 5 demo files under `demos/`.
- `ls -la` showed only `.git`, `.gitignore`, `README.md`, `demos/`, `quicksilver/`, and `tests/` before this report directory was created.
- `find . -maxdepth 3 ... pyproject.toml/setup.py/requirements/tox/nox/.github` returned no packaging, dependency, or CI files.
- `.gitignore` ignores `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`, and `*.egg-info/`.
- `git status --ignored --short` was empty after the non-mutating pytest run, so no ignored cache artifacts were left behind.

## Commands run

- `llm-tldr tree .` - confirmed the small source/test/demo shape.
- `git status --short --branch` - captured initial branch and dirty state.
- `rg --files -g '!__pycache__' -g '!*.pyc'` - listed tracked working files.
- `llm-tldr search "random|secrets|hash|serialize|pickle|eval|exec|subprocess|requests|socket|open\\(|write\\(|remove|delete|token|password|private|seed|rng|os\\.environ|dotenv" .` - found randomness, hashing, seeded demos/tests, and no network/secret-loader surface.
- `rtk read README.md`, `rtk read quicksilver/*.py`, selected `rtk read demos/*.py`, and selected `rtk read tests/*.py` - read protocol, VOLE, Fiat-Shamir, LPN, boolean, tensor, reachability, and test evidence.
- `python -m pytest --version` - failed because `python` is not installed on this machine.
- `python3 --version` - returned `Python 3.12.8`.
- `python3 -m pytest --version` - returned `pytest 9.0.3`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider` - passed with `76 passed in 0.44s`.
- Two `PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY' ... PY` reproductions - confirmed prime-field and boolean zero-challenge acceptance of malicious transcripts.
- `llm-tldr context verify --project . --lang python` - located `protocol.verify` at `quicksilver/protocol.py:251` and `boolean.verify` at `quicksilver/boolean.py:373`.
- `llm-tldr context LpnParams.default --project . --lang python` - located `LpnParams.default` at `quicksilver/lpn_vole.py:68`.
- `llm-tldr context Transcript.challenge --project . --lang python` - located `Transcript.challenge` at `quicksilver/fiat_shamir.py:96`.
- `llm-tldr context trusted_dealer_setup --project . --lang python` - located prime and boolean trusted dealer setup functions.
- `wc -l README.md quicksilver/*.py tests/*.py demos/*.py .gitignore` - counted 4,264 total lines in the audited files.

Note: I initially tried the older `llm-tldr context <file> <fn>` syntax from the global instructions; this local `llm-tldr` build expects `llm-tldr context <entry> --project .`, so the first context attempts returned usage errors and were not used as evidence.

## Local evidence inventory

- `README.md:10-12` says "About 2,500 lines", "Eight modules", "76 tests", and "six runnable demos"; local line count is 4,264 total audited lines and `demos/` contains five files.
- `README.md:110-124` shows `LpnParams.default(...)` as a drop-in VOLE PCG usage path.
- `README.md:167` says `python -m pytest tests/ -v`; local shell has no `python`, while `python3` works.
- `README.md:177-178` labels `demos/lpn_vole_demo.py` under "Real-cryptography demos".
- `README.md:185` references `demos/transitive_closure.py`, which is not present in `rg --files`.
- `README.md:201-210` explicitly says Base OT/GGM-tree single-point VOLE and performance work are still omitted.
- `quicksilver/__init__.py:6-9` states the implementation is educational and VOLE setup is performed by a trusted dealer.
- `quicksilver/vole.py:49-61` implements `trusted_dealer_setup(...)`, sampling `delta`, `u`, and `v` locally and returning both prover and verifier shares.
- `quicksilver/protocol.py:251-263` exposes `verify(..., chi, ...)` and checks assertions plus the batched check without validating that `chi` is nonzero.
- `quicksilver/protocol.py:267-272` uses `field.rand_nonzero()` in the safe `run(...)` helper.
- `quicksilver/boolean.py:373-389` exposes the same caller-supplied `chi` shape for the boolean verifier.
- `quicksilver/boolean.py:393-397` uses `mac_field.rand_nonzero()` in the safe boolean `run(...)` helper.
- `quicksilver/boolean.py:235` coerces boolean witness inputs with `int(next(wit)) & 1` rather than rejecting non-bit values.
- `quicksilver/fiat_shamir.py:78-94` binds circuit shape and gates into the transcript with a local canonical byte encoding.
- `quicksilver/fiat_shamir.py:96-112` uses SHA-256 rejection sampling and rejects zero challenge values.
- `quicksilver/lpn_vole.py:44-46` says the default `(k=2N, t=N//4)` parameters are not secure and gives real-parameter scale.
- `quicksilver/lpn_vole.py:68-72` still exposes those insecure demonstration defaults through `LpnParams.default(...)`.
- `quicksilver/lpn_vole.py:75-103` derives the public matrix from SHA-256 counter mode.
- `quicksilver/lpn_vole.py:122-133` generates the sparse base VOLE through a trusted dealer, not OT/SPCOT.
- `quicksilver/gf2k.py:10-11` says the pure-Python GF(2^128) implementation should not be used in production performance paths.
- `quicksilver/einsum.py:23-28` says the compiler materializes contractions explicitly and has no optimization passes.
- `quicksilver/zk_reachability.py:10-31` states the verifier learns only `(n, k, source, target)`, but demos print private graph/tensor data for inspection.
- `tests/test_quicksilver.py:202`, `tests/test_boolean.py:150`, `tests/test_lpn_vole.py:117`, and `tests/test_zk_reachability.py:115` use `rand_nonzero()` in tamper tests; no test covers zero-challenge rejection.
- `tests/test_fiat_shamir.py:63-77` verifies that Fiat-Shamir rejects mutated `msg1`, and `tests/test_fiat_shamir.py:84-85` verifies label/domain separation behavior.

## Risk register

### R1 - Zero challenge disables multiplication or AND soundness in direct verifier APIs

Severity: high for direct API users; contained for callers that use `run(...)` or Fiat-Shamir helpers.

Evidence:
- `quicksilver/protocol.py:251-263` and `quicksilver/boolean.py:373-389` accept caller-provided `chi` and do not reject `0`.
- `quicksilver/protocol.py:227-232` and `quicksilver/boolean.py:350-357` multiply every batched term by powers of `chi`; with `chi == 0`, all multiplication/AND terms vanish.
- `quicksilver/protocol.py:267-272`, `quicksilver/boolean.py:393-397`, and `quicksilver/fiat_shamir.py:96-112` show safer internal paths already sample/reject zero.
- Tests consistently use `rand_nonzero()`, but no test asserts `verify(..., chi=0, ...)` returns `False`.

Reproduction:
- Prime-field malicious transcript command printed `True` for `verify(..., chi=0, ...)` and `False` for `verify(..., F.rand_nonzero(), ...)`.
- Boolean malicious transcript command printed `True` for `verify(..., chi=0, ...)` and `False` for `verify(..., GF128.rand_nonzero(), ...)`.

Why it matters:
- A user who wires their own interaction layer could accidentally pass zero or use a hash-to-field routine that allows zero.
- In that case, a malicious prover can commit output/assertion values that pass assertions while the multiplication/AND relation is false.

Next safe work:
- Add guard clauses to prime, boolean, and polynomial verifier/prover batched paths rejecting `chi == 0`.
- Add regression tests that construct the malicious transcripts above and require rejection.
- Document that verifier challenges must be sampled from `F*` / `GF(2^128)*`.

### R2 - Insecure LPN defaults are public and marketed as a drop-in PCG path

Severity: high if copied into non-demo use; medium for this repo because docs disclose the caveat.

Evidence:
- `quicksilver/lpn_vole.py:44-46` says defaults are not secure and only demonstrate the technique.
- `quicksilver/lpn_vole.py:68-72` exposes `LpnParams.default(n_out)` as the ergonomic constructor.
- `README.md:110-124` shows this default path in normal usage.
- `README.md:177-178` labels the LPN demo as "Real-cryptography demos".
- `demos/lpn_vole_demo.py:28-49` demonstrates it as replacing the trusted dealer.

Why it matters:
- The code is honest about the caveat, but the shortest API path returns knowingly insecure parameters.
- "Drop-in replacement" framing can obscure that the trusted base and concrete parameter selection are still missing.

Next safe work:
- Rename `LpnParams.default` to `demo_default` or require an explicit `security_level="demo"` argument.
- Make the README example carry a visible "demo parameters only" warning next to the code block.
- Add a test that prevents silently constructing a "production" or unlabeled default.

### R3 - Trusted-dealer material is generated in-process and shares are ordinary dataclasses

Severity: medium.

Evidence:
- `quicksilver/__init__.py:6-9` and `quicksilver/vole.py:1-14` state the educational trusted-dealer model.
- `quicksilver/vole.py:49-61` returns both prover and verifier shares from a single local function.
- `quicksilver/boolean.py:61-72` does the same for subspace VOLE.
- `quicksilver/protocol.py:267-272` and `quicksilver/fiat_shamir.py:165-167` call trusted setup in end-to-end helpers.

Why it matters:
- The verifier secret `delta` is a normal dataclass field and can be logged, printed, serialized, or handed to the wrong side accidentally.
- End-to-end helpers are convenient for demos but are unsafe as deployment boundaries.

Next safe work:
- Separate demo setup helpers from protocol APIs in naming and docs.
- Add `repr=False` to secret-bearing dataclass fields or provide redacted `__repr__` methods.
- Add a deployment note saying no function in this repo performs a real distributed VOLE setup.

### R4 - Message and share length validation is partial

Severity: medium.

Evidence:
- `quicksilver/protocol.py:89`, `97`, `121`, `179`, `180`, `199`, `200`, and `210` consume VOLE/message iterators with `next(...)`.
- `quicksilver/boolean.py:228`, `236`, `256`, `307`, `308`, `325`, `326`, and `335` mirror that pattern.
- Assertion opening lengths are checked, but `d_values` exhaustion/extras and VOLE share exhaustion/extras are not normalized into verifier `False` or clear `ValueError` paths.

Why it matters:
- Malformed messages can raise `StopIteration` rather than returning `False`.
- Extra `d_values` can be ignored by interactive verify, while Fiat-Shamir absorbs all `d_values`, creating a non-canonical message surface.
- This is mostly robustness/API hardening, but cryptographic protocol APIs benefit from strict transcript shape checks.

Next safe work:
- Check expected `d_values` count against `num_inputs + num_muls` or `num_inputs + num_ands`.
- Check share lengths against `circuit.vole_count()`.
- Add tests for short and extra message/share vectors in prime and boolean verifiers.

### R5 - Boolean witness inputs are silently truncated to one bit

Severity: medium for API semantics; low for the algebraic protocol once values are bits.

Evidence:
- `quicksilver/boolean.py:235` does `x = int(next(wit)) & 1`.
- `BoolCircuit.const` and `xor_const` reject non-boolean constants at `quicksilver/boolean.py:141-158`, so witness handling is less strict than constants.

Why it matters:
- A caller passing `2` proves a statement about `0`, and `3` proves a statement about `1`.
- In demos and tests this is not dangerous, but a public API should not silently reinterpret secret inputs.

Next safe work:
- Reject witness values not in `(0, 1)`.
- Add a regression test for `run(c, [2])` raising `ValueError`.
- If coercion is intentional, document it as bit-packing behavior and provide an explicit bit-decomposition helper.

### R6 - Fiat-Shamir proof objects have no portable serialization or verifier key boundary

Severity: medium.

Evidence:
- `quicksilver/fiat_shamir.py:78-94` defines an internal circuit serialization for hashing.
- `quicksilver/fiat_shamir.py:117-120` defines `NIProof` as a Python dataclass of `CommitMessage` and `BatchedCheck`.
- `quicksilver/fiat_shamir.py:9-12` correctly states that this is designated-verifier and requires the verifier's secret `Delta`.
- There is no file format, schema version, or verifier-key container in the repo.

Why it matters:
- Non-interactive can be mistaken for publicly verifiable or portable.
- Users have to invent their own proof/share serialization, which risks inconsistent transcript binding.

Next safe work:
- Add explicit `to_bytes`/`from_bytes` or JSON schema only for demo use, or explicitly state no portable proof format is supported.
- Add docs that `NIProof` is only meaningful alongside the verifier's secret share.
- Add tests that serialization round-trips preserve transcript binding if serialization is introduced.

### R7 - Demos intentionally print private example data

Severity: low, but relevant to privacy expectations.

Evidence:
- `demos/zk_einsum.py:41-46`, `72-73`, and `110` print private matrices/graph labels for demonstration.
- `demos/zk_graph_reachability.py:74` prints graph summary, and surrounding demo code displays path/proof context.
- `quicksilver/zk_reachability.py:10-31` states the verifier learns only public `(n, k, source, target)`.

Why it matters:
- The protocol is zero-knowledge, but demos are teaching artifacts and may print inputs that the protocol would hide.
- This is fine locally, but it should not be confused with a privacy-preserving CLI.

Next safe work:
- Label demo output as "debug/private data printed for demonstration".
- Avoid printing actual private matrices in any future CLI-style entrypoint.
- Add a README distinction between protocol leakage and demo logging.

### R8 - No packaging, dependency, CI, license, or vulnerability scanning surface

Severity: medium for handoff and reproducibility; low for runtime attack surface.

Evidence:
- `find . -maxdepth 3 ... pyproject.toml/setup.py/requirements/tox/nox/.github` returned no files.
- `python -m pytest --version` failed because `python` is not installed, while README uses `python`.
- `python3 -m pytest --version` returned `pytest 9.0.3`.
- `README.md:167` documents a test command that is not portable to this machine.

Why it matters:
- There is no declared supported Python version, test dependency, license, or automated validation command.
- Future agents cannot know whether `pytest` is expected to be globally installed or whether `python3` is required.

Next safe work:
- Add `pyproject.toml` with package metadata, Python version, and test extras.
- Add a minimal CI workflow that runs the exact test command.
- Add a license file or explicitly mark the repo private/non-redistributable.

### R9 - Documentation inventory is stale in ways that can mislead audit scope

Severity: low to medium.

Evidence:
- `README.md:10-11` says eight modules and six demos.
- `rg --files quicksilver/*.py` lists 13 Python files including `__init__.py`; excluding `__init__.py`, there are 12 modules.
- `rg --files demos` lists five demo files.
- `README.md:185` references missing `demos/transitive_closure.py`.

Why it matters:
- Morning reviewers and future agents may look for a non-existent demo or under-count the protocol surface.
- Stale docs are especially risky in cryptographic repos because caveats and scope boundaries need to stay precise.

Next safe work:
- Update README inventory counts from local file lists.
- Remove or restore the `demos/transitive_closure.py` reference.
- Add a docs-claims audit task to reconcile all README security and performance claims.

### R10 - Tensor and reachability frontends have predictable performance blowups

Severity: low for security, medium for denial-of-service style local use.

Evidence:
- `quicksilver/einsum.py:23-28` says contractions are materialized explicitly and there are no optimization passes.
- `quicksilver/zk_reachability.py:32-38` documents roughly `n^2 * k` multiplication gates and pure-Python performance limits.
- `tests/test_zk_reachability.py:129-134` only checks monotonicity of small circuit sizes.

Why it matters:
- User-controlled shapes can allocate very large circuits and consume CPU/memory.
- There is no CLI/server in this repo, so this is not currently remotely exploitable, but it matters if someone wraps it.

Next safe work:
- Add optional shape/gate-count limits in high-level helpers.
- Expose a cheap `estimate_cost(...)` function for einsum and reachability APIs.
- Add tests for rejecting obviously oversized demo inputs if a CLI is introduced.

## Things that looked low risk

- No `requests`, `socket`, cloud SDK, subprocess execution, credential loader, `.env` use, or `os.environ` reads were found by the risk search.
- No destructive file operations such as `remove`, `delete`, `rmtree`, or shell command launch were found in package code.
- Randomness uses `secrets` for field sampling and VOLE material in `quicksilver/field.py`, `quicksilver/gf2k.py`, `quicksilver/boolean.py`, and `quicksilver/lpn_vole.py`.
- Fiat-Shamir transcript code binds circuit shape and gate list before deriving `chi`.
- Existing tests cover many tamper cases for normal nonzero challenges.

## Validation command candidates

- Required queue validation: `git status --short`
  - Expected after report creation: one untracked or added report file until committed by the runner; should run locally without credentials.
  - Actual before report creation: empty output.

- Strong local test proof: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider`
  - Expected: pass.
  - Actual: `76 passed in 0.44s`.

- README command as written: `python -m pytest tests/ -v`
  - Expected on this machine: fail because `python` is not installed.
  - Actual probe: `python -m pytest --version` failed with `python: command not found`.

- Demo smoke candidates:
  - `PYTHONDONTWRITEBYTECODE=1 python3 demos/quicksilver_demo.py`
  - `PYTHONDONTWRITEBYTECODE=1 python3 demos/quicksilver_boolean_demo.py`
  - `PYTHONDONTWRITEBYTECODE=1 python3 demos/lpn_vole_demo.py`
  - Expected: likely pass, but not run in this audit because the queue validation is `git status --short` and pytest already exercised the demos' protocol paths without printing private demo data.

- Security regression candidate for R1:
  - Add a focused pytest for prime and boolean `verify(..., chi=0, ...)` malicious transcripts.
  - Expected current status before fix: fail if the test asserts rejection, because current code accepts.

## Independently grabbable next tasks

### Task A - Reject zero verifier challenges everywhere

Acceptance criteria:
- `protocol.verify`, `boolean.verify`, `prove_polys`, `verify_polys`, and any public batched-check helper reject `chi == 0` with `False` or `ValueError` consistently.
- Prime and boolean malicious transcripts from this report no longer verify with zero challenge.
- Existing Fiat-Shamir and normal-run tests still pass.

Validation:
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py tests/test_lpn_vole.py -q -p no:cacheprovider`
- Add and run a new focused test file or new test cases covering `chi == 0`.

### Task B - Harden transcript/message shape validation

Acceptance criteria:
- Prime and boolean verifiers check exact `d_values`, assertion opening, and VOLE share lengths.
- Short messages return `False` or raise documented `ValueError`; extra message values are rejected, not ignored.
- Tests cover short and extra `d_values`, short shares, and extra shares for prime and boolean verifiers.

Validation:
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py tests/test_fiat_shamir.py -q -p no:cacheprovider`

### Task C - Make LPN demo defaults impossible to mistake for secure parameters

Acceptance criteria:
- `LpnParams.default` is renamed or requires an explicit demo/security-level argument.
- README code block and `demos/lpn_vole_demo.py` state "demo parameters only" next to the call site.
- Tests are updated to use the new explicit demo-default API.

Validation:
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/test_lpn_vole.py -q -p no:cacheprovider`
- `PYTHONDONTWRITEBYTECODE=1 python3 demos/lpn_vole_demo.py`

### Task D - Add reproducible project metadata

Acceptance criteria:
- Add `pyproject.toml` with supported Python version, package metadata, and pytest as a test extra or dev dependency.
- README test command uses `python3` or `python -m` only after documenting interpreter assumptions.
- Optional minimal CI workflow runs the same command.

Validation:
- `python3 -m pip install -e '.[test]'` in a fresh virtualenv, if network/package policy allows.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider`

### Task E - Reconcile stale README claims

Acceptance criteria:
- README counts match local files: module count, demo count, line-count wording, and test command.
- Missing `demos/transitive_closure.py` reference is removed or the file is restored in a separate implementation task.
- Security caveats are consolidated near all runnable cryptography examples.

Validation:
- `rg -n "six runnable|eight modules|transitive_closure|python -m pytest" README.md`
- `rg --files demos quicksilver tests`

## Non-goals for this queue item

- No product code changes.
- No generated data, caches, external service calls, deployments, pushes, or PR creation.
- No attempt to implement real Base OT/SPCOT, choose production LPN parameters, or optimize GF(2^128).
- No claim that this audit proves the cryptographic construction correct.
- No mutation of external trackers or branch status.

## Unknowns

- Whether the repo is intended to remain purely pedagogical or become a reusable library.
- Whether a license exists outside this worktree.
- Whether the upstream GitHub repo has CI, issues, or branch protection not present locally.
- Whether related sibling repos contain the missing `transitive_closure.py` or a newer README.
- Whether future users will consume only `run(...)`/`run_ni(...)` or call low-level `verify(...)` directly.
- Whether `python` being absent is local machine-specific or a standard runner property.

## Final handoff notes

- File written by this queue item: `docs/overnight/tensor-quicksilver-zk-risk-register.md`.
- Product code touched: none.
- Required validation command to run after this file exists: `git status --short`.
- Strong local validation already run: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider` with `76 passed in 0.44s`.
- PR URL: not created; PR creation is out of scope for this local audit item.
- Blockers: none for report creation. Follow-up security fixes require product-code changes and should be separate work items.
