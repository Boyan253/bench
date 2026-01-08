# bench

> Run a shell command N times and report min, median, p95 and mean - a tiny hyperfine.

## Why

`time ./thing` gives you one number, and one number from a noisy machine is not
a measurement. `bench` runs the command repeatedly and shows the spread, so you
can tell a real 20% win from scheduler noise.
