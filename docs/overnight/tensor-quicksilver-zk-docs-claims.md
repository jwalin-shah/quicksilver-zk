# Overnight docs-claims audit: tensor-quicksilver-zk

Queue item: `tensor-quicksilver-zk-docs-claims`
Focus area: `docs-claims`
Date: 2026-05-07

## Scope and repo state

This audit is read-only with respect to product code. The only intended repo
change is this report.

- Repo purpose, inferred from `README.md` and package docs: a pedagogical
  pure-Python implementation of the QuickSilver zero-knowledge protocol,
  including prime-field circuits, a GF(2^128) boolean variant, Fiat-Shamir,
  LPN-style VOLE extension, tensor-logic einsum lowering, and reachability
  demos.
- Branch observed: `codex/goal-tensor-quicksilver-zk-docs-claims`.
- Initial HEAD observed: `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.
- Initial dirty state: `git status --short --branch` printed only
  `## codex/goal-tensor-quicksilver-zk-docs-claims`; there were no modified or
  untracked entries before this report.
- Post-report dirty state before final handoff: `git status --short` is expected
  to show `?? docs/` because this report is intentionally untracked in the
  sandboxed worktree.
- Commit blocker: `git add docs/overnight/tensor-quicksilver-zk-docs-claims.md`
  failed with `Unable to create .../.git/worktrees/tensor-quicksilver-zk-docs-claims/index.lock:
  Operation not permitted`. The worktree content is writable, but the Git index
  path for this worktree lives outside the permitted writable roots. No commit
  was created; current HEAD remains `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`.
- Local issue file evidence: `items/tensor-quicksilver-zk-docs-claims/ISSUE.md`
  was not present in this worktree (`test -f ... && rtk read ... || true`
  produced no output). I used the queue item text supplied to the worker as the
  task contract.
- Repo shape evidence from `llm-tldr tree .`: top-level `README.md`,
  `quicksilver/`, `tests/`, and `demos/`; no `docs/` directory existed before
  this report.

## Commands and observations

- `llm-tldr tree .`: found 12 package implementation modules under
  `quicksilver/` excluding `__init__.py`, six test files, and five demo files.
- `rg --files -uu`: found only `.gitignore`, `README.md`, `quicksilver/*.py`,
  `tests/*.py`, and `demos/*.py`; no packaging metadata or generated docs.
- `rg --files | rg '(^|/)(pyproject\.toml|requirements.*\.txt|setup\.py|setup\.cfg|tox\.ini|noxfile\.py|Makefile|Pipfile|poetry\.lock|uv\.lock)$'`:
  no output, so there is no local dependency/install command encoded in the
  repo.
- `wc -l README.md quicksilver/*.py tests/*.py demos/*.py`: 4,259 total lines
  including README; 2,179 lines in `quicksilver/*.py`; 1,130 lines in tests;
  738 lines in demos.
- `find quicksilver -maxdepth 1 -name '*.py' ! -name '__init__.py' -print`:
  12 implementation modules, not 8.
- `find demos -maxdepth 1 -name '*.py' -print`: five demo files:
  `demos/lpn_vole_demo.py`, `demos/quicksilver_boolean_demo.py`,
  `demos/quicksilver_demo.py`, `demos/zk_einsum.py`, and
  `demos/zk_graph_reachability.py`.
- `find tests -maxdepth 1 -name 'test_*.py' -print`: six test files.
- `rg -n '^def test_' tests | wc -l`: 76 test functions.
- `python -m pytest --collect-only -q tests`: failed because this shell has no
  `python` executable (`python: command not found`).
- `python3 -m pytest tests/ -v`: passed, `76 passed in 0.44s`.
- Demo validation with `python3`:
  `demos/quicksilver_demo.py`, `demos/zk_graph_reachability.py`,
  `demos/zk_einsum.py`, `demos/quicksilver_boolean_demo.py`, and
  `demos/lpn_vole_demo.py` all completed successfully. The LPN demo's largest
  scaling case reported `n_out=2048`, `k_base=4096`, and `setup(ms)=21331.2`,
  so it is a real smoke test but not as cheap as the others.
- `ls -la demos/transitive_closure.py`: failed with `No such file or directory`.
- `../agent-stack-docs-claims/repos.json` lists `tensor-quicksilver-zk` and
  sibling `tensor-logic` in the `tensor` group. Read-only sibling evidence:
  `/Users/jwalinshah/projects/tensor/tensor-logic/demos/transitive_closure.py`
  does exist and contains the recurrence
  `Path = step( Edge + einsum('xy,yz->xz', Path, Edge) )`.
- Read-only sibling dirty state:
  `git -C /Users/jwalinshah/projects/tensor/tensor-logic status --short --branch`
  reported modified files and untracked claim docs, so cross-repo handoffs
  should not assume a clean sibling checkout.

## Docs claim audit

### Supported or mostly supported

- `README.md` describes a pedagogical QuickSilver implementation. This is
  supported by `quicksilver/__init__.py`, which explicitly calls the project
  educational and says VOLE setup is by trusted dealer rather than production
  OT/LPN preprocessing.
- `README.md` claims 76 tests across six files. This is supported by
  `tests/test_boolean.py`, `tests/test_einsum.py`,
  `tests/test_fiat_shamir.py`, `tests/test_lpn_vole.py`,
  `tests/test_quicksilver.py`, and `tests/test_zk_reachability.py`; pytest
  collected and passed 76 tests.
- The "no third-party dependencies" runtime claim is mostly supported for the
  package and demos: imports in `quicksilver/*.py` are stdlib plus internal
  package imports. Caveat: tests require `pytest`, and the repo has no
  `pyproject.toml` or requirements file to tell a new worker how to get it.
- The IT-MAC explanation in `README.md` matches `quicksilver/itmac.py`, which
  implements `K = M + Delta * x`, local linear operations, `prover_commit`,
  `verifier_receive`, and `open_to_zero`.
- The "linear operations are free" and "multiplication gates are batched"
  claims are supported by `quicksilver/circuit.py` and
  `quicksilver/protocol.py`: `vole_count()` is
  `num_inputs + num_muls + 1`; linear gates do not increment `num_muls`; the
  prover and verifier aggregate multiplication checks in `batched_check` and
  `check_batched`.
- The polynomial extension claim is supported by `quicksilver/polynomial.py`
  and tests in `tests/test_quicksilver.py`, including cubic, multivariate,
  batched quadratic, and soundness-negative cases.
- The boolean GF(2^128) claim is supported by `quicksilver/boolean.py`,
  `quicksilver/gf2k.py`, and `tests/test_boolean.py`, including XOR chains,
  AND soundness, assertion tampering, and 4-bit multiplier coverage.
- The Fiat-Shamir non-interactive proof claim is supported by
  `quicksilver/fiat_shamir.py` and `tests/test_fiat_shamir.py`. The module
  correctly narrows the claim: this remains designated-verifier and is not
  public verifiability.
- The einsum/reachability examples are materially supported by
  `quicksilver/einsum.py`, `quicksilver/zk_reachability.py`,
  `tests/test_einsum.py`, `tests/test_zk_reachability.py`,
  `demos/zk_einsum.py`, and `demos/zk_graph_reachability.py`.

### Unsupported, stale, or needs qualification

- `README.md` says "Eight modules"; the package currently has 12
  implementation modules excluding `__init__.py`:
  `boolean.py`, `circuit.py`, `einsum.py`, `fiat_shamir.py`, `field.py`,
  `gf2k.py`, `itmac.py`, `lpn_vole.py`, `polynomial.py`, `protocol.py`,
  `vole.py`, and `zk_reachability.py`.
- `README.md` says "six runnable demos"; the local repo has five demo files.
  All five passed with `python3`, but there is no sixth local demo.
- The README run block uses `python`, but this local environment only has
  `python3`. The documented command fails here; the equivalent `python3`
  commands pass.
- `README.md` references `demos/transitive_closure.py` as if it is local. That
  file is absent here. It exists in sibling `tensor-logic`, but the README does
  not qualify this as a sibling-repo reference.
- The "About 2,500 lines of Python" claim is ambiguous. It is close if the
  claim means package implementation only (2,179 lines in `quicksilver/*.py`);
  it is false if a reader interprets it as all Python in the repo (4,047 lines
  across package, tests, and demos).
- "Designated-verifier zero-knowledge proofs for arbitrary circuits over any
  field" is directionally aligned with the paper but broader than this code.
  The code has a prime-field path via `Fp` and a separate GF(2^128) boolean
  path. It does not implement a general finite-field registry, arbitrary field
  backends, or production field choices.
- "`einsum.py` generalises this: any tensor-logic rule head expressible as an
  einsum is automatically a QuickSilver circuit" is too broad without caveats.
  `quicksilver/einsum.py` handles explicit einsum specs over flat tensors and
  public expected outputs; it does not parse the `tensor-logic` rule language,
  stratified negation, provenance, threshold semantics, disjunctions, or
  lookups.
- The README says LPN-based VOLE is a drop-in for the trusted dealer. The code
  supports the API shape and tests it, but `quicksilver/lpn_vole.py` explicitly
  says defaults `(k=2N, t=N//4)` are not secure and that base OT/SPCOT is not
  implemented. The README's caveat section mentions missing base OT and
  performance, but does not foreground that the demo defaults are not concrete
  security parameters.

### Non-claims worth preserving

- The README does not claim production readiness. It explicitly calls out pure
  Python performance limits, no FFT/vectorization, and missing base OT/GGM-tree
  single-point VOLE.
- The Fiat-Shamir module does not claim public verifiability; it correctly
  notes designated-verifier verification still requires the verifier secret
  `Delta`.
- The repo does not claim packaging support, CI support, or installability.
  Those are absent rather than contradicted.

## Risks and stale assumptions

1. README inventory drift can mislead follow-on workers. The top summary says
   eight modules and six demos, while the local evidence is 12 package modules
   and five demos.
2. Copy-paste onboarding is brittle. The README's validation command uses
   `python`, but the local worker environment only has `python3`; there is no
   `pyproject.toml`, requirements file, Makefile, or tox/nox entry to define
   a canonical setup.
3. Security posture is easy to overread. Soundness comments and README field
   sizes look cryptographic, while VOLE setup is trusted-dealer, LPN defaults
   are explicitly not secure, side-channel behavior is not considered, and no
   production parameter table exists.
4. Cross-repo tensor-logic references are under-specified. The missing local
   `demos/transitive_closure.py` reference is backed only by sibling
   `tensor-logic`, whose checkout is currently dirty; this creates handoff
   risk if a worker tries to validate the README inside this repo only.
5. The "any tensor-logic rule head expressible as an einsum" wording risks
   collapsing two APIs. This repo has an einsum-to-circuit helper; sibling
   `tensor-logic` has rule parsing and thresholded Datalog semantics. They are
   related but not one integrated frontend.
6. Performance claims are mostly qualitative. The demos pass quickly except
   the LPN scaling demo's 2048 case, which took about 21 seconds locally. There
   is no benchmark harness or expected runtime envelope.

## Next safe work

### Task 1: Fix README inventory and local validation commands

Acceptance criteria:

- README summary reports the actual module and demo counts, or stops giving
  exact counts that are likely to drift.
- README run commands use `python3` or document the `python` assumption.
- The local `demos/transitive_closure.py` reference is removed, qualified as
  a sibling `tensor-logic` reference, or backed by a local file.

Validation commands:

- `python3 -m pytest tests/ -v` should pass with 76 tests.
- `python3 demos/quicksilver_demo.py` should pass.
- `python3 demos/zk_graph_reachability.py` should pass.
- `python3 demos/zk_einsum.py` should pass.
- `python3 demos/quicksilver_boolean_demo.py` should pass.
- `python3 demos/lpn_vole_demo.py` should pass, with expected runtime in the
  tens of seconds on this machine.
- `git status --short` should show only intended README/docs changes.

### Task 2: Add a security and cryptographic-scope caveat document

Acceptance criteria:

- A short docs page or README section states clearly: pedagogical code, trusted
  dealer setup, no base OT/SPCOT, LPN defaults not secure, designated verifier,
  no public verification, no side-channel hardening, no audited production
  parameters.
- The page links to `quicksilver/vole.py`, `quicksilver/lpn_vole.py`,
  `quicksilver/fiat_shamir.py`, and `quicksilver/gf2k.py` as local evidence.
- README top summary points to the caveat before quoting cryptographic-looking
  soundness numbers.

Validation commands:

- `rg -n "trusted dealer|not secure|designated-verifier|public verifiability|side-channel|production" README.md docs quicksilver`
  should show the caveats in docs and the implementation notes.
- `python3 -m pytest tests/test_lpn_vole.py tests/test_fiat_shamir.py -v`
  should pass.
- `git status --short` should show only the intended docs changes.

### Task 3: Make the tensor-logic handoff explicit

Acceptance criteria:

- README distinguishes the local QuickSilver einsum compiler from sibling
  `tensor-logic`'s Datalog/rule-language tooling.
- The transitive-closure recurrence is either included as a local snippet with
  no fake local file path, or the README points to the sibling repo path
  explicitly.
- Unsupported rule-language features are named: negation, thresholds,
  provenance, disjunctions/lookups, and full tensor-logic parser integration.

Validation commands:

- `rg -n "transitive_closure|tensor-logic|einsum|Datalog|negation|lookup|provenance" README.md quicksilver`
  should show qualified claims rather than a broken local file reference.
- `python3 -m pytest tests/test_einsum.py tests/test_zk_reachability.py -v`
  should pass.
- `git status --short` should show only intended docs changes.

### Task 4: Add a minimal local setup contract

Acceptance criteria:

- Repo has one canonical install/test path, either a minimal `pyproject.toml`
  with `pytest` in a dev extra or a plain `requirements-dev.txt`.
- README validation uses that contract.
- Runtime package remains third-party-free unless a deliberate dependency is
  added.

Validation commands:

- `python3 -m pip install -e ".[dev]"` or the chosen equivalent should work in
  a fresh virtual environment.
- `python3 -m pytest tests/ -v` should pass.
- `python3 -c "import quicksilver; print(quicksilver.__all__)"`
  should pass.

## Validation command candidates

- Queue validation: `git status --short`.
  Expected in this sandbox after writing the report: exit 0 with `?? docs/`,
  because staging/committing is blocked by Git index permissions outside the
  writable roots.
- README test command as written: `python -m pytest tests/ -v`.
  Expected in this worker shell: fail, because `python` is not installed.
- Correct local test command: `python3 -m pytest tests/ -v`.
  Observed: pass, `76 passed in 0.44s`.
- Fast docs-claim proof subset:
  `python3 -m pytest tests/test_einsum.py tests/test_zk_reachability.py tests/test_fiat_shamir.py -v`.
  Expected: pass; covers the most claim-heavy README sections without running
  every test.
- Demo proof: run all five `python3 demos/*.py` commands individually.
  Observed: all pass; LPN scaling is the slowest at about 21 seconds for the
  largest printed case.

## Non-goals

- No product-code changes.
- No generated data, external services, deploys, pushes, or PR creation.
- No attempt to prove the QuickSilver math from first principles or compare
  implementation details against the full CCS paper.
- No attempt to repair the sibling `tensor-logic` dirty state.
- No benchmark normalization beyond recording observed demo runtimes.

## Unknowns

- The queue's `issue_file` path was absent in this worktree; the queue prompt
  supplied the issue body, so this did not block the audit.
- There is no CI metadata in this repo, so the canonical validation environment
  is unknown.
- I did not verify whether another branch already fixes the stale README
  counts or broken transitive-closure path.
- I did not validate on a clean machine without globally installed `pytest`.
- I did not inspect external papers or current cryptographic parameter tables;
  cryptographic-security statements here are limited to local code/docs
  evidence.
- I could not create a local commit from this sandbox because Git needs to write
  an index lock under the source checkout's `.git/worktrees/` directory, which
  is outside the writable roots for this worker.
