"""Shared verifier challenge validation tests."""

from __future__ import annotations

from quicksilver.challenge import is_nonzero_field_challenge
from quicksilver.field import F
from quicksilver.gf2k import GF128


def test_prime_field_challenge_must_be_nonzero_field_element():
    assert is_nonzero_field_challenge(1, F)
    assert is_nonzero_field_challenge(F.p - 1, F)

    assert not is_nonzero_field_challenge(0, F)
    assert not is_nonzero_field_challenge(-1, F)
    assert not is_nonzero_field_challenge(F.p, F)
    assert not is_nonzero_field_challenge(True, F)
    assert not is_nonzero_field_challenge("1", F)


def test_binary_mac_field_challenge_must_be_nonzero_field_element():
    assert is_nonzero_field_challenge(1, GF128)
    assert is_nonzero_field_challenge(GF128.p - 1, GF128)

    assert not is_nonzero_field_challenge(0, GF128)
    assert not is_nonzero_field_challenge(GF128.p, GF128)
    assert not is_nonzero_field_challenge(True, GF128)
