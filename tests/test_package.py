"""Package-level import and export checks."""

from __future__ import annotations

import quicksilver


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
