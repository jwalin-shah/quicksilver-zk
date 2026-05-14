"""Package-level import and export checks."""

from __future__ import annotations

import quicksilver
from quicksilver import cli
from quicksilver.cli import build_parser, run_demo, run_quick_validation


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


def test_quick_validation_fails_when_guarded_step_fails(monkeypatch):
    calls = []

    def fake_pytest():
        calls.append("pytest")
        return 0

    def fake_demo(name):
        calls.append(name)
        return 7 if name == "zk_einsum.py" else 0

    monkeypatch.setattr(cli, "run_pytest", fake_pytest)
    monkeypatch.setattr(cli, "run_demo", fake_demo)

    assert run_quick_validation() == 7
    assert calls == ["pytest", "quicksilver_demo.py", "zk_einsum.py"]
