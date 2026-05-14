"""Package-level import and export checks."""

from __future__ import annotations

import quicksilver
from quicksilver.cli import build_parser, run_demo


def test_package_exports_public_api():
    assert quicksilver.__all__ == [
        "F",
        "Fp",
        "Wire",
        "Circuit",
        "prove",
        "verify",
        "run",
    ]
    for name in quicksilver.__all__:
        assert hasattr(quicksilver, name)


def test_package_cli_parses_demo_command():
    parser = build_parser()
    ns = parser.parse_args(["demo", "quicksilver_demo.py"])
    assert ns.command == "demo"
    assert ns.name == "quicksilver_demo.py"
    assert run_demo("does_not_exist") == 1
