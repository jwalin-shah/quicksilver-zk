"""Package-level CLI for QuickSilver convenience commands."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from typing import Iterable, List


_ROOT = Path(__file__).resolve().parents[1]
_DEMO_NAMES = (
    "quicksilver_demo.py",
    "zk_einsum.py",
    "zk_graph_reachability.py",
    "quicksilver_boolean_demo.py",
    "lpn_vole_demo.py",
)


def _demo_paths() -> List[Path]:
    return [_ROOT / "demos" / name for name in _DEMO_NAMES]


def _run(argv: Iterable[str], *, cwd: Path | None = None) -> int:
    cmd = [sys.executable, *argv]
    proc = subprocess.run(cmd, cwd=str(cwd or _ROOT))
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
    return _run(["-m", "pytest", "tests", "-q"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m quicksilver",
        description="QuickSilver package utilities.",
    )
    sub = parser.add_subparsers(dest="command")
    sp_demo = sub.add_parser("demo", help="Run demos (all or one)")
    sp_demo.add_argument("name", nargs="?", default="all")
    sub.add_parser("test", help="Run test suite via pytest")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "demo":
        return run_demo(args.name)
    if args.command == "test":
        return run_pytest()
    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
