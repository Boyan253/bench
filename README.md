# bench

> Run a shell command N times and report min, median, p95 and mean - a tiny hyperfine.

## Why

`time ./thing` gives you one number, and one number from a noisy machine is not
a measurement. `bench` runs the command repeatedly and shows the spread, so you
can tell a real 20% win from scheduler noise.

## Usage

```
python bench.py -n 20 -- python build.py
python bench.py -n 50 -w 5 -- ./target/release/parser input.txt
python bench.py --shell -n 10 -- "cat big.log | grep ERROR | wc -l"
```

## Output

```
runs   20 (after 1 warmup)
min    412.8 ms
p50    431.1 ms
p95    498.0 ms
max    512.4 ms
mean   439.7 ms
stdev   24.9 ms
```

Compare **p50** between two builds, not `min` and not `mean`: the median is
what a user actually experiences, and it is not dragged around by one unlucky
run.

## Notes

- Warmup runs are executed and discarded, so caches and JITs are not measured.
- A non-zero exit from the command aborts the benchmark — you cannot
  accidentally benchmark a crash.
- Command output is discarded so terminal I/O is not part of the timing.
- `--shell` if you need pipes or redirection; without it the command is
  executed directly, which is more accurate.

## Tests

```
pip install pytest
pytest
```
