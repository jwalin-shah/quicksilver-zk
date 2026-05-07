# tensor-quicksilver-zk risk and validation review

Queue item: `tensor-quicksilver-zk-risk-and-validation-review`
Branch: `codex/goal-tensor-quicksilver-zk-risk-and-validation-review`
Baseline commit inspected: `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`
Review date: 2026-05-07

## Scope

This was a read-only risk and validation pass over the local
`tensor-quicksilver-zk` worktree. No product code was changed. The only
intended repo change is this report under `docs/overnight/2026-05-07-whole-portfolio-review/`.

No previous overnight reports or runner outputs were available in this repo:
`git ls-files docs runs items .agent-stack-worktrees` returned no tracked files.

## Validation run

- `llm-tldr tree .` completed and showed a compact repo with `quicksilver/`,
  `tests/`, `demos/`, and `README.md`.
- `git status --short` before report creation returned no output.
- `python -m pytest tests/ -v` failed locally with exit 127 because `python`
  is not on PATH: `/opt/homebrew/bin/bash: line 1: python: command not found`.
- `python3 -m pytest tests/ -v` passed: 76 tests collected, 76 passed in 0.45s
  on Python 3.12.8 with pytest 9.0.3.
- `python3 demos/quicksilver_demo.py` passed all prime-field demos.
- `python3 demos/quicksilver_boolean_demo.py` passed all boolean demos; the
  10-bit multiplier scaling row took about 247 ms.
- `python3 demos/lpn_vole_demo.py` passed, but its default scaling demo reached
  about 20.6 s at `n_out=2048`.
- `python3 demos/zk_einsum.py` passed all einsum-ZK demos.
- `python3 demos/zk_graph_reachability.py` passed all reachability demos.

Required queue validation to rerun after this report is written:

```bash
git status --short
```

## Concrete observations

1. `README.md` advertises "no third-party dependencies", "Eight modules",
   "76 tests", and "six runnable demos"; the tracked tree currently has 12
   `quicksilver/*.py` files including `__init__.py`, 7 test files including
   `tests/test_zk_reachability.py`, and 5 demo files under `demos/`.
2. `README.md` documents `python -m pytest tests/ -v`, but this environment
   only has `python3`; the documented command failed before pytest could run.
3. `README.md` mentions `demos/transitive_closure.py`, but no such tracked
   file exists.
4. `.gitignore` covers `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.venv/`,
   and `*.egg-info/`, but there is no tracked `pyproject.toml`,
   `requirements.txt`, `setup.py`, `setup.cfg`, `tox.ini`, or CI workflow.
5. `quicksilver/protocol.py` consumes `msg.d_values` and `share.w` through
   iterators and `next(...)` calls in `_VerifierWalker.receive`; malformed
   short inputs can raise `StopIteration`, while extra `d_values` are ignored.
6. `quicksilver/boolean.py` silently coerces boolean witness inputs with
   `int(next(wit)) & 1`, so a witness value like `2` is accepted as bit `0`
   instead of being rejected as malformed input.
7. `quicksilver/fiat_shamir.py` does bind circuit shape, gates, `d_values`,
   and assertion openings into the transcript, and the tests cover msg1/msg2
   tampering and label mismatch. Its integer encoding is fixed at 32 bytes,
   so very large public constants or future fields larger than 256 bits can
   fail during transcript absorption before verification.
8. `quicksilver/lpn_vole.py` explicitly says the default LPN parameters are
   not secure and still rely on trusted dealer base correlations; `README.md`
   labels the demo section "Real-cryptography demos", which can overstate the
   implementation's deployment readiness.
9. `quicksilver/einsum.py` intentionally materializes contractions directly
   with no optimization passes; tests cover small matmul, dot, trace, outer,
   and three-tensor cases, but there is no guardrail for accidental huge
   contraction blowups.
10. `quicksilver/zk_reachability.py` documents and demos `O(n^2 * k)` circuit
    growth; tests check monotonic growth, while demos show `n=16,k=5` reaching
    1408 multiplication gates in about 20.5 ms.
11. `tests/test_quicksilver.py`, `tests/test_boolean.py`,
    `tests/test_fiat_shamir.py`, and `tests/test_zk_reachability.py` include
    useful negative tests for wrong witnesses and tampered batched checks.
12. `tests/test_lpn_vole.py` validates correlation preservation, deterministic
    matrix derivation, seeded variance, protocol integration, and oversized
    Hamming weight rejection, but it does not enforce a security profile or
    prevent insecure demo parameters from looking production-ready.

## Risks and blockers

- Validation reproducibility is not pinned. The suite passes under `python3`,
  but the README's exact command fails locally and there is no project config
  or CI file defining the supported Python versions and test entrypoint.
- Malformed proof handling is not canonical. Prime-field and boolean verifiers
  should reject short or extra message/share data predictably rather than
  raising iterator exceptions or ignoring trailing data.
- Boolean witness input validation is too permissive because non-bit witness
  values are truncated to parity.
- Fiat-Shamir serialization is good enough for the current 127-bit field but
  has fixed-width integer assumptions that become brittle for large constants
  or future field variants.
- The README has stale inventory claims and one missing demo reference, which
  makes it risky to use as the source of truth for future workers.
- LPN VOLE is clearly marked educational in code comments, but README wording
  can still invite a false security interpretation.
- No previous overnight reports, local `runs/*/result.json`, or local
  `runs/*/handoff.md` existed in this repo to compare against.

## Implementation-ready follow-up tasks

### 1. Add a reproducible validation entrypoint

Owned files: `pyproject.toml`, `.github/workflows/ci.yml`, `README.md`.

Acceptance criteria:

- The repo declares supported Python versions and a pytest/dev dependency path.
- The documented local test command works on this machine without relying on a
  `python` alias.
- CI runs the same pytest command and a syntax/import smoke check.
- README inventory is updated to the actual module, test-file, and demo counts.

Smallest useful validation:

```bash
python3 -m pytest tests/ -v
python3 -m compileall quicksilver demos tests
```

### 2. Reject malformed proof and share lengths canonically

Owned files: `quicksilver/protocol.py`, `quicksilver/boolean.py`,
`tests/test_quicksilver.py`, `tests/test_boolean.py`,
`tests/test_fiat_shamir.py`.

Acceptance criteria:

- Prime-field and boolean verifiers reject short `d_values`, extra `d_values`,
  short VOLE verifier shares, and extra assertion openings by returning
  `False` or raising a documented `ValueError`, consistently across APIs.
- Existing valid proof, tamper, and Fiat-Shamir tests still pass.
- New tests cover short and trailing message data for both protocols.

Smallest useful validation:

```bash
python3 -m pytest tests/test_quicksilver.py tests/test_boolean.py tests/test_fiat_shamir.py -v
```

### 3. Validate boolean witness bits instead of truncating them

Owned files: `quicksilver/boolean.py`, `tests/test_boolean.py`,
`demos/quicksilver_boolean_demo.py`.

Acceptance criteria:

- Boolean prover input values must be exactly `0` or `1`.
- Non-bit witness values raise `ValueError` with a clear message.
- Existing boolean demos and tests continue to pass with valid bit witnesses.

Smallest useful validation:

```bash
python3 -m pytest tests/test_boolean.py -v
python3 demos/quicksilver_boolean_demo.py
```

### 4. Harden Fiat-Shamir transcript serialization

Owned files: `quicksilver/fiat_shamir.py`, `tests/test_fiat_shamir.py`,
`tests/test_quicksilver.py`.

Acceptance criteria:

- Transcript integer encoding is length-delimited and handles arbitrary-size
  non-negative field elements and signed circuit constants.
- Large public constants in a circuit can be proven and verified without
  `OverflowError`.
- Existing label mismatch, msg1 tamper, and msg2 tamper tests still fail closed.

Smallest useful validation:

```bash
python3 -m pytest tests/test_fiat_shamir.py tests/test_quicksilver.py -v
```

### 5. Add frontend guardrails for tensor and reachability inputs

Owned files: `quicksilver/einsum.py`, `quicksilver/zk_reachability.py`,
`tests/test_einsum.py`, `tests/test_zk_reachability.py`.

Acceptance criteria:

- Invalid einsum specs such as duplicate output labels, missing tensor data,
  or ragged nested tensors raise `ValueError` before circuit construction.
- `assemble_witness` rejects every non-binary edge-matrix entry, not only the
  entries used by the claimed path.
- Tests cover both accepted valid examples and rejected malformed inputs.

Smallest useful validation:

```bash
python3 -m pytest tests/test_einsum.py tests/test_zk_reachability.py -v
```

