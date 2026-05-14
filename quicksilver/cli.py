"""Package-level CLI for QuickSilver convenience commands."""

from __future__ import annotations

import argparse
import importlib
import os
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
_QUICK_VALIDATION_DEMOS = (
    "quicksilver_demo.py",
    "zk_einsum.py",
)
_SMOKE_MODULES = (
    "quicksilver",
    "quicksilver.boolean",
    "quicksilver.circuit",
    "quicksilver.protocol",
)


def _demo_paths() -> List[Path]:
    return [_ROOT / "demos" / name for name in _DEMO_NAMES]


def _run(argv: Iterable[str], *, cwd: Path | None = None) -> int:
    cmd = [sys.executable, *argv]
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(_ROOT) if not pythonpath else os.pathsep.join((str(_ROOT), pythonpath))
    )
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
        print(
            f"Unknown demo {demo!r}. Expected one of: {', '.join(names)}",
            file=sys.stderr,
        )
        return 1
    target = _ROOT / "demos" / demo
    if not target.exists():
        print(f"Demo file is missing: {target}", file=sys.stderr)
        return 1
    return _run([str(target)])


def run_pytest() -> int:
    return _run(["-m", "pytest", "tests", "-q"])


def run_cli_smoke() -> int:
    """Cheap no-secret check for imports, argument parsing, and demo registry."""
    for module in _SMOKE_MODULES:
        importlib.import_module(module)

    parser = build_parser()
    args = parser.parse_args(["demo", "quicksilver_demo.py"])
    if args.command != "demo" or args.name != "quicksilver_demo.py":
        print("CLI parser smoke failed for demo command", file=sys.stderr)
        return 1

    missing = [path.name for path in _demo_paths() if not path.exists()]
    if missing:
        print(f"CLI smoke missing demo files: {', '.join(missing)}", file=sys.stderr)
        return 1

    print("QuickSilver CLI smoke passed.")
    return 0


def run_quick_validation() -> int:
    """Run the local pre-handoff validation gate used by CI."""
    rc = run_cli_smoke()
    if rc != 0:
        return rc

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
    sub.add_parser("smoke", help="Run a cheap CLI import/parser smoke check")
    sub.add_parser("test", help="Run test suite via pytest")
    sub.add_parser("quick-validate", help="Run the local pre-handoff gate")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "demo":
        return run_demo(args.name)
    if args.command == "smoke":
        return run_cli_smoke()
    if args.command == "test":
        return run_pytest()
    if args.command == "quick-validate":
        return run_quick_validation()
    parser.print_help()
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
