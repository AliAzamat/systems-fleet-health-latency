# Fleet Health & Latency Checks

**A small, dependency-free Python toolkit that answers "is the fleet healthy, and which node is slow?" — TCP connect latency with p50/p99 and jitter, loss accounting, DNS timing, gateway and "port actually answers" checks, concurrent probing, and a JSON report whose exit code carries the verdict.**

For latency-sensitive systems, averages hide the problem: two nodes with the same median can differ wildly in their tail. This toolkit measures the tail, treats failed connects as loss rather than letting them skew latency stats, and turns the numbers into a `healthy` / `degraded` / `down` verdict that automation can act on. It's a diagnostic tool, not a port scanner.

## What it measures

| Check | Module | How |
|---|---|---|
| Connect latency | `probe.py` | Full TCP connect timed with a monotonic clock (`perf_counter`); `None` on failure or timeout |
| Percentiles | `percentiles.py` | Nearest-rank p50/p99 over successful samples only; failures counted separately as loss |
| Jitter | `jitter.py` | Sample standard deviation alongside p50 and p99 |
| DNS | `netcheck.py` | Time to resolve a hostname |
| Gateway | `netcheck.py` | TCP reachability of the default gateway (port 179 by default) |
| Liveness | `netcheck.py` | Port is open **and** returns at least one byte to a probe — "open but mute" fails |
| Fleet fan-out | `fleet.py`, `bounded.py` | `asyncio.gather` over thread-offloaded probes; a semaphore (default 256) caps in-flight sockets to avoid exhausting file descriptors |
| Verdict | `report.py` | `down` if no successes, loss > 10%, or p99 > 50 ms; `degraded` if loss > 1% or p99 > 5 ms |

## Usage

Requires Python 3.10+; standard library only.

```bash
git clone https://github.com/AliAzamat/systems-fleet-health-latency.git
cd systems-fleet-health-latency
```

```python
from cli import main

exit_code = main([("10.0.1.11", 9001), ("10.0.1.12", 9001)])
```

Each node is sampled 50 times and reported as JSON:

```text
{
  "nodes": [
    { "host": "10.0.1.11", "p50_ms": <ms>, "p99_ms": <ms>, "loss": <fraction>, "status": "healthy" | "degraded" | "down" },
    { "host": "10.0.1.12", "p50_ms": null, "p99_ms": null, "loss": 1.0, "status": "down" }
  ]
}
```

The second entry is exactly what an unreachable port produces (checked against a closed local port).

The exit code is the contract for shells, CI steps, and deploy gates:

| Exit | Meaning |
|---|---|
| `0` | All nodes healthy |
| `1` | At least one node degraded |
| `2` | At least one node down |

For a quick concurrent sweep without sampling, `fleet.run(targets)` or `bounded.check_fleet_bounded(targets, limit=256)` returns one connect latency per host.

## Design notes

- **p99 over mean.** Thresholds are on the tail because that's what a latency-sensitive caller experiences.
- **Loss is not latency.** Folding timeouts into latency samples would both inflate the stats and hide the failure rate; they're tracked separately.
- **Bounded concurrency.** Unbounded fan-out to thousands of nodes opens thousands of sockets at once; the semaphore lets work proceed up to a limit.
