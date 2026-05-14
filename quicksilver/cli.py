"""Package-level CLI for QuickSilver convenience commands."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from typing import Iterable, List


_ROOT = Path(__file__).resolve().parents[1]
_RUNTIME_DIR_ENV = "QUICKSILVER_RUNTIME_DIR"
_RUNTIME_DIR_DEFAULT = ".quicksilver-runtime"
_DEMO_NAMES = (
    "quicksilver_demo.py",
    "zk_einsum.py",
    "zk_graph_reachability.py",
    "quicksilver_boolean_demo.py",
    "lpn_vole_demo.py",
)
_QUICK_VALIDATION_DEMOS = (
    "quicksilver_demo.py",
    "zk_einsum.py",
)


def _demo_paths() -> List[Path]:
    return [_ROOT / "demos" / name for name in _DEMO_NAMES]


def _runtime_dir() -> Path:
    configured = os.environ.get(_RUNTIME_DIR_ENV, _RUNTIME_DIR_DEFAULT)
    return Path(configured).expanduser()


def _run(argv: Iterable[str], *, cwd: Path | None = None) -> int:
    cmd = [sys.executable, *argv]
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(_ROOT) if not pythonpath else os.pathsep.join((str(_ROOT), pythonpath))
    )
    runtime_dir = _runtime_dir()
    if not runtime_dir.is_absolute():
        runtime_dir = _ROOT / runtime_dir
    env.setdefault("PYTHONPYCACHEPREFIX", str(runtime_dir / "pycache"))
    proc = subprocess.run(cmd, cwd=str(cwd or _ROOT), env=env)
    return proc.returncode


def run_demo(demo: str = "all") -> int:
    """Run one demo or all demos shipped with the repo."""
    demos = _demo_paths()
    names = [Path(path).name for path in demos]

    if demo == "all":
        for path in demos:
            rc = _run([str(path)])
            if rc != 0:
                return rc
        return 0

    if demo not in names:
        return 1
    target = _ROOT / "demos" / demo
    if not target.exists():
        return 1
    return _run([str(target)])


def run_pytest() -> int:
    runtime_dir = _runtime_dir()
    cache_dir = runtime_dir / "pytest-cache"
    return _run(["-m", "pytest", "tests", "-q", "-o", f"cache_dir={cache_dir}"])


def run_quick_validation() -> int:
    """Run the local pre-handoff validation gate used by CI."""
    rc = run_pytest()
    if rc != 0:
        return rc

    for demo in _QUICK_VALIDATION_DEMOS:
        rc = run_demo(demo)
        if rc != 0:
            return rc
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m quicksilver",
        description="QuickSilver package utilities.",
    )
    sub = parser.add_subparsers(dest="command")
    sp_demo = sub.add_parser("demo", help="Run demos (all or one)")
    sp_demo.add_argument("name", nargs="?", default="all")
    sub.add_parser("test", help="Run test suite via pytest")
    sub.add_parser("quick-validate", help="Run the local pre-handoff gate")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "demo":
        return run_demo(args.name)
    if args.command == "test":
        return run_pytest()
    if args.command == "quick-validate":
        return run_quick_validation()
    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
