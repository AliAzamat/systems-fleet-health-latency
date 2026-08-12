import asyncio
from probe import tcp_connect_ms

# Run one node's latency probe without blocking the event loop: the blocking
# socket call is pushed to a thread, so hundreds can be "in flight" at once.
async def probe_node(host: str, port: int) -> tuple[str, float | None]:
    loop = asyncio.get_running_loop()
    ms = await loop.run_in_executor(None, tcp_connect_ms, host, port)
    return host, ms

# Check the whole fleet CONCURRENTLY. With 100 nodes this finishes in roughly
# the time of the single slowest node, not the sum of all of them.
async def check_fleet(targets: list[tuple[str, int]]) -> dict[str, float | None]:
    tasks = [probe_node(host, port) for host, port in targets]
    results = await asyncio.gather(*tasks)
    return {host: ms for host, ms in results}

def run(targets: list[tuple[str, int]]) -> dict[str, float | None]:
    return asyncio.run(check_fleet(targets))
