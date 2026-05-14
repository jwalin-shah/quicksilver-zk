"""Package-level import and export checks."""

from __future__ import annotations

import subprocess
import sys

import quicksilver
from quicksilver import cli
from quicksilver.cli import build_parser, run_cli_smoke, run_demo, run_quick_validation


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


def test_package_cli_smoke_contract(capsys):
    assert run_cli_smoke() == 0
    assert "QuickSilver CLI smoke passed." in capsys.readouterr().out


def test_package_cli_smoke_does_not_require_source_tree_demos(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "_ROOT", tmp_path)

    assert run_cli_smoke() == 0
    captured = capsys.readouterr()
    assert "QuickSilver CLI smoke passed." in captured.out
    assert captured.err == ""


def test_package_cli_smoke_entrypoint_runs_without_secrets():
    proc = subprocess.run(
        [sys.executable, "-m", "quicksilver", "smoke"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0
    assert "QuickSilver CLI smoke passed." in proc.stdout
    assert proc.stderr == ""


def test_package_cli_bad_demo_reports_clear_failure():
    proc = subprocess.run(
        [sys.executable, "-m", "quicksilver", "demo", "missing_demo.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 1
    assert "Unknown demo 'missing_demo.py'." in proc.stderr
    assert "quicksilver_demo.py" in proc.stderr


def test_quick_validation_fails_when_guarded_step_fails(monkeypatch):
    calls = []

    def fake_smoke():
        calls.append("smoke")
        return 0

    def fake_pytest():
        calls.append("pytest")
        return 0

    def fake_demo(name):
        calls.append(name)
        return 7 if name == "zk_einsum.py" else 0

    monkeypatch.setattr(cli, "run_cli_smoke", fake_smoke)
    monkeypatch.setattr(cli, "run_pytest", fake_pytest)
    monkeypatch.setattr(cli, "run_demo", fake_demo)

    assert run_quick_validation() == 7
    assert calls == ["smoke", "pytest", "quicksilver_demo.py", "zk_einsum.py"]
