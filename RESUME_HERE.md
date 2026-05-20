# Resume Here

Status: **SHIPPED / EXPERIMENT**. This repo is a pedagogical artifact, not an
active product workstream. No active work is needed.

## What This Implements

This repository implements a pure-Python teaching version of the QuickSilver
zero-knowledge proof system:

- Prime-field arithmetic over the Mersenne prime `2^127 - 1`.
- Trusted-dealer VOLE preprocessing and information-theoretic MAC wires.
- An arithmetic-circuit DSL plus prover/verifier logic for QuickSilver-style
  designated-verifier proofs.
- Batched multiplication checks and polynomial relation checks.
- A boolean-circuit path over `GF(2^128)`.
- Fiat-Shamir transcript support for a non-interactive designated-verifier
  proof object.
- A toy LPN-style VOLE extension demo.
- Tensor-logic frontends for einsum constraints and graph reachability proofs.
- Five runnable demos and a package-level validation command.

The code is intentionally small and dependency-light. It is meant to make the
protocol mechanics inspectable, runnable, and testable rather than fast or
production-secure.

## Why It Exists

This repo exists to show the core QuickSilver idea in executable form:

- Linear circuit operations are local operations on MACed values.
- Multiplication gates are checked with a single batched verifier challenge.
- Polynomial constraints can be checked without expanding everything into
  intermediate multiplication wires.
- Tensor/einsum rules can be compiled into ZK circuit constraints, making the
  relationship between tensor logic and proof systems concrete.

It is useful as a reference, explainer, and experiment bed for protocol and
frontend ideas. It is not intended to be a deployable cryptographic library.

## Current State

- Package metadata exists in `pyproject.toml`.
- The canonical local validation entrypoint is:

  ```bash
  make quick-validate PYTHON=python3
  ```

- The test suite currently collects 91 tests with:

  ```bash
  python3 -m pytest --collect-only -q tests/
  ```

- The README documents the protocol, layout, demos, usage examples, and
  security boundaries.

## No Active Work Needed

Do not treat this file as a queue. There is no current milestone, blocker, or
handoff task to continue.

Future changes should only be made if a new explicit task is created. Good
candidate categories would be documentation corrections, small pedagogical
examples, or focused validation improvements. Avoid broad production-hardening
work unless the repo is deliberately re-scoped.
