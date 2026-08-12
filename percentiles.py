from probe import tcp_connect_ms

# Compute the value at a given percentile from a list of samples. p=50 is the
# median; p=99 is "99% of connects were at least this fast." We use the
# nearest-rank method: sort, then index to the rank.
def percentile(samples: list[float], p: float) -> float:
    if not samples:
        raise ValueError("no samples")
    ordered = sorted(samples)
    # nearest-rank: rank = ceil(p/100 * N), then 1-based index into the sorted list
    rank = max(1, (len(ordered) * p + 99) // 100)  # integer ceil of p% of N
    return ordered[int(rank) - 1]

# Connect N times and collect only the SUCCESSFUL latencies. Failed connects
# are counted separately as loss — they must not pollute the latency stats.
def sample_latencies(host: str, port: int, n: int = 50) -> tuple[list[float], int]:
    oks: list[float] = []
    failures = 0
    for _ in range(n):
        ms = tcp_connect_ms(host, port)
        if ms is None:
            failures += 1
        else:
            oks.append(ms)
    return oks, failures
