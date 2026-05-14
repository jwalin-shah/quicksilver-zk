"""Verifier challenge validation shared by protocol variants."""

from __future__ import annotations

from typing import Protocol


class FieldWithOrder(Protocol):
    p: int


def is_nonzero_field_challenge(chi: object, field: FieldWithOrder) -> bool:
    """Return whether ``chi`` is a non-zero element of ``field``."""
    return type(chi) is int and 0 < chi < field.p
