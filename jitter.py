import math

# Jitter = how much latency VARIES from sample to sample. Two nodes can share a
# median of 0.4ms while one is rock-steady and the other swings 0.1–5ms. The
# steady one is far more useful to a trading system. We measure it as the
# standard deviation of the successful latencies.
def stddev(samples: list[float]) -> float:
    if len(samples) < 2:
        return 0.0
    mean = sum(samples) / len(samples)
    variance = sum((x - mean) ** 2 for x in samples) / (len(samples) - 1)
    return math.sqrt(variance)

# A node's latency profile: typical level (p50), tail (p99), and jitter (stddev).
# Together they describe not just "how fast" but "how predictable".
def latency_profile(samples: list[float]) -> dict:
    from percentiles import percentile
    return {
        "p50_ms": round(percentile(samples, 50), 3),
        "p99_ms": round(percentile(samples, 99), 3),
        "jitter_ms": round(stddev(samples), 3),
    }
