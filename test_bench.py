import sys

import pytest

import bench

NOOP = [sys.executable, "-c", "pass"]


def test_percentile_p50():
    assert bench.percentile([1, 2, 3, 4, 5], 0.5) == 3

def test_percentile_edges():
    values = list(range(1, 101))
    assert bench.percentile(values, 0.95) == 95
    assert bench.percentile(values, 1.0) == 100


def test_percentile_single_value():
    assert bench.percentile([7], 0.95) == 7

def test_percentile_empty_raises():
    with pytest.raises(ValueError):
        bench.percentile([], 0.5)


def test_summarise_fields():
    stats = bench.summarise([1.0, 2.0, 3.0])
    assert stats["runs"] == 3
    assert stats["min"] == 1.0
    assert stats["max"] == 3.0
    assert stats["mean"] == 2.0

def test_fmt_scales_units():
    assert bench.fmt(0.0000005).endswith("us")
    assert bench.fmt(0.05).endswith("ms")
    assert bench.fmt(2.5).endswith("s")
