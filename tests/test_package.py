"""Package-level import and export checks."""

from __future__ import annotations

import os

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


def test_cli_subprocesses_use_ignored_runtime_cache(monkeypatch):
    calls = []

    def fake_run(cmd, cwd, env):
        calls.append((cmd, cwd, env))

        class Proc:
            returncode = 0

        return Proc()

    monkeypatch.delenv("QUICKSILVER_RUNTIME_DIR", raising=False)
    monkeypatch.delenv("PYTHONPYCACHEPREFIX", raising=False)
    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    assert cli._run(["-c", "pass"]) == 0
    _, cwd, env = calls[0]
    assert cwd == str(cli._ROOT)
    assert env["PYTHONPYCACHEPREFIX"] == str(
        cli._ROOT / ".quicksilver-runtime" / "pycache"
    )


def test_pytest_cache_defaults_to_ignored_runtime_dir(monkeypatch):
    called = []

    def fake_run(argv):
        called.append(argv)
        return 0

    monkeypatch.delenv("QUICKSILVER_RUNTIME_DIR", raising=False)
    monkeypatch.setattr(cli, "_run", fake_run)

    assert cli.run_pytest() == 0
    assert called == [
        [
            "-m",
            "pytest",
            "tests",
            "-q",
            "-o",
            "cache_dir=.quicksilver-runtime/pytest-cache",
        ]
    ]


def test_runtime_dir_can_be_overridden(monkeypatch, tmp_path):
    custom = tmp_path / "runtime"
    monkeypatch.setenv("QUICKSILVER_RUNTIME_DIR", os.fspath(custom))
    assert cli._runtime_dir() == custom


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
