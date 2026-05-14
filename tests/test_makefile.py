"""Makefile runtime path checks."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_makefile_pycache_prefix_respects_absolute_runtime_dir(tmp_path):
    runtime_dir = tmp_path / "runtime"

    proc = subprocess.run(
        [
            "make",
            "--dry-run",
            "quick-validate",
            f"QUICKSILVER_RUNTIME_DIR={runtime_dir}",
            "PYTHON=python3",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert f"PYTHONPYCACHEPREFIX={runtime_dir / 'pycache'}" in proc.stdout
    assert f"PYTHONPYCACHEPREFIX={ROOT}/{runtime_dir}/pycache" not in proc.stdout
