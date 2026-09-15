#!/usr/bin/env python3
"""Time a command over several runs and report the distribution."""

import argparse
import math
import statistics
import subprocess
import sys
import time

__version__ = "0.1.0"


def percentile(values, fraction):
    """Nearest-rank percentile: the smallest value at or above `fraction` of the data.

    Always returns a real observation rather than an interpolation, so p50 of
    four samples is a timing that actually happened.
    """
    if not values:
        raise ValueError("no values")
    ordered = sorted(values)
    rank = max(1, min(len(ordered), math.ceil(fraction * len(ordered))))
    return ordered[rank - 1]


def summarise(samples):
    return {
        "runs": len(samples),
        "min": min(samples),
        "p50": percentile(samples, 0.50),
        "p95": percentile(samples, 0.95),
        "max": max(samples),
        "mean": statistics.fmean(samples),
        "stdev": statistics.pstdev(samples) if len(samples) > 1 else 0.0,
    }


def fmt(seconds):
    if seconds < 1e-3:
        return "%.0f us" % (seconds * 1e6)
    if seconds < 1:
        return "%.1f ms" % (seconds * 1e3)
    return "%.3f s" % seconds


def run_once(command, shell=False):
    start = time.perf_counter()
    proc = subprocess.run(command, shell=shell, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
    return time.perf_counter() - start, proc.returncode


def bench(command, runs=10, warmup=1, shell=False, on_sample=None):
    for _ in range(warmup):
        run_once(command, shell)
    samples = []
    for i in range(runs):
        elapsed, code = run_once(command, shell)
        if code != 0:
            raise RuntimeError("command exited with %d on run %d" % (code, i + 1))
        samples.append(elapsed)
        if on_sample:
            on_sample(i + 1, elapsed)
    return samples


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("-n", "--runs", type=int, default=10)
    ap.add_argument("-w", "--warmup", type=int, default=1)
    ap.add_argument("--shell", action="store_true", help="run through the shell")
    ap.add_argument("command", nargs=argparse.REMAINDER,
                    help="the command, after --")
    args = ap.parse_args(argv)

    command = [c for c in args.command if c != "--"]
    if not command:
        ap.error("give a command, e.g. bench.py -n 5 -- ls -la")
    if args.shell:
        command = " ".join(command)

    def progress(i, elapsed):
        print("  run %d/%d  %s" % (i, args.runs, fmt(elapsed)), file=sys.stderr)

    try:
        samples = bench(command, args.runs, args.warmup, args.shell, progress)
    except RuntimeError as exc:
        print("bench: %s" % exc, file=sys.stderr)
        return 1

    stats = summarise(samples)
    print("runs   %d (after %d warmup)" % (stats["runs"], args.warmup))
    for key in ("min", "p50", "p95", "max", "mean"):
        print("%-6s %s" % (key, fmt(stats[key])))
    print("stdev  %s" % fmt(stats["stdev"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
