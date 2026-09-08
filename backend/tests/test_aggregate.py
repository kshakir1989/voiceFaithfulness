import pytest

from app.domain.aggregate import overall_percentage, round_display


def test_overall_none_when_empty():
    assert overall_percentage([]) is None


def test_overall_mean():
    assert overall_percentage([80.0, 100.0]) == 90.0


def test_round_display():
    assert round_display(87.56) == 87.6
    assert round_display(None) is None
