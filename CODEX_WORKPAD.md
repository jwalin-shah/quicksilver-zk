# CODEX Workpad

## MAX-267 Quick Validation CI (2026-05-11)

- Branch: `codex/MAX-267-quicksilver-quick-validation-ci`
- Worktree: `/Users/jwalinshah/projects/tensor/quicksilver-zk-MAX-267`
- Base: `origin/main` at `cb83568`
- Plan:
  - Add PR CI for the documented quick validation command.
  - Keep the slow LPN scaling demo out of the default CI lane.
  - Document that PR CI uses the same quick-validation target.
- Files touched:
  - `.github/workflows/ci.yml`
  - `README.md`
  - `CODEX_WORKPAD.md`
- Validation:
  - `make quick-validate PYTHON=python3` passed: 78 tests plus `quicksilver_demo.py` and `zk_einsum.py`.
- Pending:
  - Commit, push, open PR, and update `MAX-267`.
