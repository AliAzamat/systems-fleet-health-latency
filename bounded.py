import asyncio
from probe import tcp_connect_ms

# An asyncio.Semaphore caps how many probes are IN FLIGHT at once. Without it,
# fanning out to 5,000 nodes opens 5,000 sockets simultaneously — exhausting
# file descriptors and overwhelming the checker host. The semaphore lets work
# proceed up to `limit`, then makes the rest wait their turn.
async def probe_bounded(sem: asyncio.Semaphore, host: str, port: int):
    async with sem:                      # acquire a slot; released on exit
        loop = asyncio.get_running_loop()
        ms = await loop.run_in_executor(None, tcp_connect_ms, host, port)
        return host, ms

async def check_fleet_bounded(targets, limit: int = 256):
    sem = asyncio.Semaphore(limit)       # at most `limit` probes at once
    tasks = [probe_bounded(sem, h, p) for h, p in targets]
    results = await asyncio.gather(*tasks)
    return {host: ms for host, ms in results}
