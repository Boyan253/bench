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
