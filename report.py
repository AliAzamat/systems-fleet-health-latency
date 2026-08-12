import json
from percentiles import sample_latencies, percentile

# Thresholds that define health for a latency-sensitive node. Tunable per fleet;
# these are the policy that turns raw numbers into a verdict.
P99_DEGRADED_MS = 5.0     # p99 above this → degraded
P99_DOWN_MS = 50.0        # p99 above this → effectively down
LOSS_DEGRADED = 0.01      # >1% loss → degraded
LOSS_DOWN = 0.10          # >10% loss → down

# Classify one node from its latency samples + loss into healthy/degraded/down.
def classify(p99: float | None, loss: float) -> str:
    if p99 is None or loss > LOSS_DOWN or p99 > P99_DOWN_MS:
        return "down"
    if loss > LOSS_DEGRADED or p99 > P99_DEGRADED_MS:
        return "degraded"
    return "healthy"

# Build a structured report for one node: the raw numbers AND the verdict.
def node_report(host: str, port: int, n: int = 50) -> dict:
    oks, failures = sample_latencies(host, port, n)
    loss = failures / n
    p99 = percentile(oks, 99) if oks else None
    p50 = percentile(oks, 50) if oks else None
    return {
        "host": host,
        "p50_ms": round(p50, 3) if p50 is not None else None,
        "p99_ms": round(p99, 3) if p99 is not None else None,
        "loss": round(loss, 3),
        "status": classify(p99, loss),
    }

# A fleet report is a JSON document — machine-readable so a dashboard or alerting
# system can scrape it, not a pretty string for a human to eyeball.
def fleet_report(targets: list[tuple[str, int]]) -> str:
    nodes = [node_report(h, p) for h, p in targets]
    return json.dumps({"nodes": nodes}, indent=2)
