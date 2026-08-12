import sys
import json
from report import node_report

# A health check is only useful in automation if its EXIT CODE carries the
# verdict — that's the contract every shell, CI step, and deploy gate reads.
#   exit 0  → all nodes healthy
#   exit 1  → at least one node degraded (warn)
#   exit 2  → at least one node down (fail)
def main(targets: list[tuple[str, int]]) -> int:
    reports = [node_report(h, p) for h, p in targets]
    # JSON to stdout for machines/humans; the verdict goes in the exit code.
    print(json.dumps({"nodes": reports}, indent=2))

    statuses = {r["status"] for r in reports}
    if "down" in statuses:
        return 2          # hard fail — something is down
    if "degraded" in statuses:
        return 1          # warn — something is slow/lossy
    return 0              # all healthy

if __name__ == "__main__":
    # targets would be parsed from argv / the fleet manifest in practice
    fleet = [("10.0.1.11", 9001), ("10.0.1.12", 9001), ("10.0.1.13", 9001)]
    sys.exit(main(fleet))
