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
