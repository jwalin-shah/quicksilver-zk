# tensor-quicksilver-zk Architecture Map

Queue item: `tensor-quicksilver-zk-architecture-map`
Branch: `codex/goal-tensor-quicksilver-zk-architecture-map`
Repo path: `/Users/jwalinshah/projects/agent-stack/.agent-stack-worktrees/2026-05-07-overnight-marathon/tensor-quicksilver-zk-architecture-map`
Audit focus: architecture-map

## Scope

This was a read-only architecture audit except for this report. I did not edit
product code, generated data, secrets, deploy configuration, external services,
or trackers. I did not create a PR.

Initial dirty state:

- `git status --short --branch` returned only
  `## codex/goal-tensor-quicksilver-zk-architecture-map`.
- `git status --short` returned no output.

Observed dirty state after this report:

- `git status --short` returned `?? docs/`.
- `rg --files docs` returned exactly
  `docs/overnight/tensor-quicksilver-zk-architecture-map.md`.

HEAD at audit time: `60b7fbe9c27f3e6ff925b8fc15927a9f31507b54`

## Commands Run

Architecture and file inventory:

- `llm-tldr tree .`
- `rg --files | sort`
- `wc -l README.md quicksilver/*.py demos/*.py tests/*.py`
- `wc -l quicksilver/*.py | tail -1`
- `rg --files quicksilver | wc -l`
- `rg --files demos | wc -l`
- `rg -n "^(class|def|async def)|^    def |^@dataclass|^if __name__" quicksilver demos tests`
- `rg -n "^(from|import) " quicksilver demos tests`
- `llm-tldr arch .`
- `llm-tldr context prove --project . --depth 2`
- `llm-tldr context verify --project . --depth 2`
- `llm-tldr context Circuit --project . --depth 2`
- `rtk read README.md`
- `rtk read quicksilver/__init__.py`
- `rtk read quicksilver/field.py`
- `rtk read quicksilver/gf2k.py`
- `rtk read quicksilver/vole.py`
- `rtk read quicksilver/itmac.py`
- `rtk read quicksilver/circuit.py`
- `rtk read quicksilver/protocol.py`
- `rtk read quicksilver/polynomial.py`
- `rtk read quicksilver/fiat_shamir.py`
- `rtk read quicksilver/lpn_vole.py`
- `rtk read quicksilver/einsum.py`
- `rtk read quicksilver/boolean.py`
- `rtk read quicksilver/zk_reachability.py`

Validation and environment probes:

- `git log --oneline -5`
- `git rev-parse HEAD`
- `git status --short`
- `rg --files docs`
- `rtk diff git diff` failed with `rtk: No such file or directory (os error 2)`;
  the report file is untracked, so this did not affect validation.
- `PYTHONDONTWRITEBYTECODE=1 python -c "import quicksilver"` failed because
  `python` is not available in this local environment.
- `PYTHONDONTWRITEBYTECODE=1 python3 -c "import quicksilver; print(quicksilver.__all__)"`
  succeeded and printed `['F', 'Fp', 'Wire', 'Circuit', 'prove', 'verify', 'run']`.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider`
  passed: `76 passed in 0.46s`.

Exploration mistakes corrected during the audit:

- `llm-tldr context quicksilver/protocol.py prove` failed because the installed
  `llm-tldr context` command expects the symbol as the positional entry.
- `llm-tldr impact quicksilver/circuit.py`, `llm-tldr impact quicksilver/protocol.py`,
  and `llm-tldr impact quicksilver/boolean.py` failed because the command expects
  a function entry rather than a file path.

## Repository Shape

The repo is a compact pure-Python educational implementation:

- `README.md`
- `quicksilver/`: 13 Python files including `__init__.py`, 2179 lines by `wc`.
- `tests/`: 6 test files plus `tests/__init__.py`, 76 `def test_...` functions.
- `demos/`: 5 runnable Python files.

There are no matched packaging or automation files from this search:

- `pyproject.toml`
- `setup.py`
- `setup.cfg`
- `requirements*.txt`
- `tox.ini`
- `pytest.ini`
- `Makefile`
- `.github/**`
- `mypy.ini`
- `ruff.toml`
- `.pre-commit-config.yaml`

The tests and demos compensate by inserting the repo root into `sys.path`, for
example in `tests/test_quicksilver.py`, `tests/test_boolean.py`,
`demos/quicksilver_demo.py`, and the other demo/test entrypoints.

## Entrypoints

Public package entrypoint:

- `quicksilver/__init__.py` exports only the prime-field arithmetic protocol
  surface: `F`, `Fp`, `Wire`, `Circuit`, `prove`, `verify`, and `run`.

Direct module entrypoints:

- Prime-field circuit proving: `quicksilver.circuit.Circuit` plus
  `quicksilver.protocol.prove`, `verify`, and `run`.
- Non-interactive designated-verifier proofs:
  `quicksilver.fiat_shamir.prove_ni`, `verify_ni`, and `run_ni`.
- Polynomial extension: `quicksilver.polynomial.Polynomial`,
  `prove_polys`, `verify_polys`, and `run_poly_check`.
- Boolean protocol: `quicksilver.boolean.BoolCircuit`, `prove`, `verify`,
  `run`, and its local `trusted_dealer_setup`.
- Tensor frontend: `quicksilver.einsum.compile_einsum`,
  `assert_einsum_equals`, `evaluate_einsum`, and allocation helpers.
- Graph reachability frontend: `quicksilver.zk_reachability.build_circuit`,
  `assemble_witness`, and `prove_path`.
- Demo entrypoints under `demos/*.py`, each guarded by `if __name__ == "__main__"`.
- Test files can also self-run via `pytest.main([__file__, "-v"])`.

Local entrypoint note: the README uses `python -m pytest tests/ -v`, but this
worktree only has `python3` available. The equivalent local command with cache
and bytecode disabled passed.

## Module Boundary Map

### Base Arithmetic

`quicksilver/field.py` owns the prime-field abstraction. The interface exposes
plain-int operations through the singleton `F = Fp(p=(1 << 127) - 1)`.

`quicksilver/gf2k.py` owns GF(2^128) arithmetic for boolean MACs. It presents a
similar operation shape to `Fp`, but its `p` attribute is only compatibility
surface; the field size is exposed as `order`.

Boundary observation: the two field modules intentionally share method names
but do not share a formal protocol or base class. That keeps the implementation
small, but callers must know which arithmetic laws apply.

### VOLE and IT-MAC Preprocessing

`quicksilver/vole.py` owns prime-field trusted-dealer VOLE shares:

- `VoleProverShare(u, v)`
- `VoleVerifierShare(delta, w)`
- `trusted_dealer_setup`

`quicksilver/lpn_vole.py` is a drop-in producer of those same share dataclasses
using an LPN-style expansion. It depends on `field.py` and `vole.py`, and the
public compatibility point is the returned `VoleProverShare` /
`VoleVerifierShare`.

`quicksilver/itmac.py` owns prime-field IT-MAC wire views:

- `ProverWire(x, m)`
- `VerifierWire(k)`
- commit/receive/constant/open helpers
- `Wire = ProverWire` as package sugar

Boundary observation: the prime protocol has a clear preprocessing seam because
both trusted-dealer and LPN expansion return the same VOLE share types.

### Arithmetic Circuit DSL

`quicksilver/circuit.py` owns the arithmetic circuit description:

- `Op`
- `Gate`
- `Circuit`

The `Circuit` interface is intentionally small: inputs, constants, linear
operations, multiplication, zero/equality assertions, and `vole_count()`.
Wire references are plain integer ids. The circuit object is a mutable append-only
gate list consumed by prover and verifier in lockstep.

Boundary observation: `Circuit` is the central statement IR. It does not validate
wire provenance, gate topological order, or malformed wire ids at construction
time; those errors surface later during protocol walking.

### Prime-Field Interactive Protocol

`quicksilver/protocol.py` owns the three-round arithmetic protocol:

- message dataclasses: `CommitMessage`, `BatchedCheck`
- private walkers: `_ProverWalker`, `_VerifierWalker`
- public API: `prove`, `verify`, `run`

The walkers consume the same `Circuit.gates` list in lockstep. Inputs and mul
outputs consume VOLE elements; assertions open zero tags; the final VOLE element
masks the batched multiplication check.

Boundary observation: this is the deepest module in the prime-field stack. It
hides most protocol complexity behind `prove`, `verify`, and `run`, but tests
still import `_ProverWalker` and `_VerifierWalker` directly in
`tests/test_quicksilver.py` to inspect internal wire views. That is evidence the
current public interface is not enough for some valid test/extension needs.

### Polynomial Extension

`quicksilver/polynomial.py` owns Section 5 degree-d polynomial checks:

- `Polynomial`
- `PolyProof`
- `prove_polys`
- `verify_polys`
- `run_poly_check`

It depends directly on `ProverWire`, `VerifierWire`, and VOLE shares. It does
not depend on `Circuit` or `protocol.py`.

Boundary observation: this module is mathematically an extension of the protocol,
but architecturally it sits beside the protocol and requires existing
`prover_wires` / `verifier_wires` dictionaries. That creates a leaky seam:
callers need access to committed wire views that `protocol.prove` and
`protocol.verify` normally keep inside private walkers.

### Fiat-Shamir Adapter

`quicksilver/fiat_shamir.py` owns the non-interactive designated-verifier
adapter for arithmetic circuits:

- `Transcript`
- `NIProof`
- `prove_ni`
- `verify_ni`
- `run_ni`

It binds the circuit and first prover message into a SHA-256 transcript, derives
`chi`, then delegates proof verification back to `protocol.verify`.

Boundary observation: this adapter wraps the prime-field `Circuit` protocol. It
does not wrap the boolean protocol or the separate polynomial-extension API.

### Boolean Protocol

`quicksilver/boolean.py` owns the GF(2^128) boolean stack in one file:

- subspace VOLE shares and trusted setup
- boolean IT-MAC wire views
- `BoolCircuit`, `BOp`, `BGate`
- `_BProverWalker`, `_BVerifierWalker`
- `prove`, `verify`, `run`

The module depends only on `quicksilver.gf2k`. It does not reuse `Circuit`,
`itmac`, `vole`, or `protocol`.

Boundary observation: boolean proving is isolated, which avoids forcing a weak
shared abstraction across prime and binary arithmetic. The tradeoff is duplicated
protocol structure: the batch-check walker pattern, message shape, assertion
handling, and VOLE-count assumptions exist independently in `protocol.py` and
`boolean.py`.

### Tensor and Graph Frontends

`quicksilver/einsum.py` owns tensor-rule lowering into the arithmetic `Circuit`.
It parses an einsum spec, resolves dimensions, emits mul/add gates, and offers a
reference evaluator for tests/demos.

`quicksilver/zk_reachability.py` owns a specific graph-reachability statement.
It builds a `Circuit`, returns a `ReachabilityCircuit` metadata object, assembles
witnesses in the same input order that `build_circuit` used, and offers
`prove_path`.

Boundary observation: these modules are frontends, not proof engines. Their main
architectural risk is witness-order coupling: `assemble_witness` must exactly
match `build_circuit`'s `c.input()` order, and `einsum` callers manually flatten
tensors to the same row-major order expected by the compiler.

## Dependency Direction

The import scan and `llm-tldr arch .` found no circular dependencies.

Observed direction:

- `field.py` and `gf2k.py` are leaves.
- `vole.py` depends on `field.py`.
- `itmac.py` depends on `field.py`.
- `lpn_vole.py` depends on `field.py` and `vole.py`.
- `circuit.py` has no project imports.
- `protocol.py` depends on `circuit.py`, `field.py`, `itmac.py`, and `vole.py`.
- `fiat_shamir.py` depends on `circuit.py`, `field.py`, `protocol.py`, and
  `vole.py`.
- `polynomial.py` depends on `field.py`, `itmac.py`, and `vole.py`.
- `boolean.py` depends on `gf2k.py`.
- `einsum.py` depends on `circuit.py`.
- `zk_reachability.py` depends on `circuit.py`, `field.py`, and `protocol.py`.
- `tests/` and `demos/` are top-level consumers.

`llm-tldr arch .` summarized directory layers as:

- `demos`: high entry/controller layer, `calls_in: 0`
- `tests`: high entry/controller layer, `calls_in: 0`
- `quicksilver`: low utility/data layer, `calls_in: 215`
- circular dependencies: `[]`

## Ownership Map

Current ownership seams:

- Prime-field core protocol: `field.py`, `vole.py`, `itmac.py`, `circuit.py`,
  `protocol.py`.
- Alternate prime VOLE source: `lpn_vole.py`.
- Protocol extension over committed wires: `polynomial.py`.
- Non-interactive adapter over prime circuits: `fiat_shamir.py`.
- Boolean protocol family: `gf2k.py`, `boolean.py`.
- Statement frontends: `einsum.py`, `zk_reachability.py`.
- Human-facing examples and proof scenarios: `demos/`.
- Regression and soundness checks: `tests/`.

The strongest interface is `Circuit` plus `protocol.run/prove/verify`: callers
get a small surface and do not need to know about IT-MAC internals.

The weakest interface is polynomial checking over already-committed wires:
`polynomial.py` expects wire dictionaries that are currently internal walker
state. Tests reach into `_ProverWalker` and `_VerifierWalker`, which confirms
that this seam is real and not just theoretical.

## Stale or Load-Bearing Assumptions

README inventory drift:

- `README.md` says "Eight modules, 76 tests, six runnable demos."
- Local evidence shows 13 Python files under `quicksilver/` including
  `__init__.py`, and 5 files under `demos/`.
- The 76-test claim is supported by `rg -n "^def test_" tests | wc -l` and by
  the passing pytest run.

Missing referenced demo:

- `README.md`, `demos/zk_graph_reachability.py`,
  `demos/zk_einsum.py`, and `quicksilver/zk_reachability.py` refer to
  `transitive_closure.py`.
- `rg --files | sort` shows no `demos/transitive_closure.py` or other file by
  that name.

Runtime command assumption:

- The README's validation command uses `python`, but this local worktree has no
  `python` executable.
- `python3` works.

Packaging assumption:

- Tests and demos insert the repo root into `sys.path`.
- No packaging metadata or runner config was found.
- This makes local script execution straightforward, but it means the public
  package import path is not validated through an installable package boundary.

Protocol-surface assumption:

- `fiat_shamir.py` provides non-interactivity for the prime-field circuit
  protocol only.
- The boolean protocol and polynomial extension do not share this adapter.

## Architecture Friction

1. Polynomial checks need committed wire views, but the prime protocol hides
   those views inside private walkers.

   Evidence:

   - `polynomial.py` APIs accept `prover_wires` and `verifier_wires` dictionaries.
   - `protocol.py` keeps those dictionaries on `_ProverWalker` and
     `_VerifierWalker`.
   - `tests/test_quicksilver.py` imports `_ProverWalker` and `_VerifierWalker`
     directly for `test_walker_produces_consistent_views`.

   Impact:

   - Extensions that need committed-wire state must either bypass the public
     protocol API or duplicate setup/commit logic.
   - Future protocol changes can silently break polynomial callers that depend
     on private walker internals.

2. Boolean proving is a parallel protocol implementation, not a variant of the
   arithmetic protocol.

   Evidence:

   - `boolean.py` defines local share dataclasses, circuit/gate classes, message
     dataclasses, walkers, setup, `prove`, `verify`, and `run`.
   - It imports only `gf2k.py`.

   Impact:

   - This is a reasonable educational split, but protocol fixes must be audited
     twice.
   - There is no shared conformance suite for message length handling,
     assertion behavior, malformed witnesses, or batch-check tampering across
     prime and boolean paths.

3. Witness layout is coupled to circuit construction order.

   Evidence:

   - `Circuit.input()` appends gates and increments `num_inputs`.
   - `protocol._ProverWalker.commit()` consumes witness values by iterating
     gates.
   - `zk_reachability.assemble_witness()` manually emits edge entries and then
     intermediate frontier entries in the same order as `build_circuit()`.
   - `einsum.flatten_row_major()` is the caller-side convention that must match
     `compile_einsum()`.

   Impact:

   - The current examples are small and well tested, but frontend authors can
     accidentally produce a syntactically valid witness with the wrong semantic
     layout.
   - A future frontend would benefit from an explicit statement layout object or
     generated witness packer.

4. Message and share shape validation is mostly implicit.

   Evidence:

   - `protocol._VerifierWalker.receive()` iterates over `msg.d_values` and
     `share.w`, but does not check for leftover values after walking the circuit.
   - `protocol._ProverWalker.commit()` reserves the final mask by calling
     `next(vole)` and relies on `StopIteration` if a share is short.
   - `boolean.py` follows a similar walker pattern.

   Impact:

   - Honest flows are tested and pass.
   - Malformed proofs and share-size mismatches can fail with low-level iterator
     behavior or accept ignored surplus data, making the protocol boundary harder
     to reason about.

5. Boolean witness values are coerced instead of validated.

   Evidence:

   - `boolean._BProverWalker._exec()` handles inputs with `x = int(next(wit)) & 1`.
   - `BoolCircuit.const()` validates constants as `0` or `1`, but input witness
     values are silently reduced to their low bit.

   Impact:

   - The module docstring says wire values are bits.
   - Silent witness coercion can hide caller bugs and makes the boolean circuit
     boundary weaker than its constant boundary.

## Validation Notes

Confirmed locally:

- `PYTHONDONTWRITEBYTECODE=1 python3 -c "import quicksilver; print(quicksilver.__all__)"`
  passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider`
  passed with `76 passed in 0.46s`.

Required queue validation:

- Command: `git status --short`
- Final result after writing this report: `?? docs/`
- `rg --files docs` showed exactly one report file:
  `docs/overnight/tensor-quicksilver-zk-architecture-map.md`

Missing or weak validation surface:

- No package metadata validates editable install or installed-package imports.
- No lint/type/format configuration was found.
- README demo count cannot be validated because one referenced demo file is
  missing.
- No CI configuration was found locally.

## Next Safe Work

1. Create a packaging and validation harness.

   Acceptance criteria:

   - Add minimal `pyproject.toml` for package metadata and pytest dependency.
   - Update tests/demos to run without per-file `sys.path.insert` hacks when the
     package is installed editable.
   - README validation command uses the executable that works locally or documents
     both `python` and `python3`.
   - Validation: `python3 -m pytest tests/ -q`.

2. Tighten the prime protocol public boundary.

   Acceptance criteria:

   - `verify` rejects surplus and undersized `CommitMessage.d_values` explicitly.
   - `prove` and `verify` raise clear `ValueError` messages for undersized VOLE
     shares rather than leaking `StopIteration`.
   - Add tests for surplus message data, short shares, and malformed assertion
     openings.
   - Validation: targeted `python3 -m pytest tests/test_quicksilver.py -q`.

3. Make polynomial extension use a deliberate committed-wire interface.

   Acceptance criteria:

   - Introduce a small public helper or trace object that exposes committed
     prover/verifier wire views after the commit phase without importing private
     walkers in tests or demos.
   - Update polynomial tests to avoid direct `_ProverWalker` /
     `_VerifierWalker` imports.
   - Document whether polynomial checks are intentionally outside
     `fiat_shamir.py` or add a non-interactive adapter for them.
   - Validation: `python3 -m pytest tests/test_quicksilver.py tests/test_fiat_shamir.py -q`.

4. Decide and document the boolean protocol ownership boundary.

   Acceptance criteria:

   - Add tests proving non-binary boolean witnesses are rejected or explicitly
     document the current low-bit coercion behavior.
   - Add parity tests for malformed message/share shapes across `protocol.py`
     and `boolean.py`.
   - Decide whether `BoolCircuit` and `quicksilver.boolean.run` should remain
     module-only or be exported from `quicksilver/__init__.py`.
   - Validation: `python3 -m pytest tests/test_boolean.py -q`.

## Blockers

No blockers for this audit. Future work that touches packaging, public API, or
protocol behavior should be handled as separate implementation issues because
this queue item is scoped to one read-only architecture report.
