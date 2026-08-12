# Fleet Health & Latency Checks: Know Your Nodes in Milliseconds

An intermediate systems project that builds the operational health layer a latency-sensitive shop lives on. This is not a security port scanner — it is the diagnostic tool that answers "is the fleet healthy right now, and which node is slow?" You measure TCP connect latency with a socket and a clock, learn why p99 matters far more than the average for trading, compute percentiles honestly, resolve and time DNS, verify the default gateway and routing, and check that a service port is not just open but actually answering. You fan the checks out concurrently across many nodes with asyncio, classify each node healthy / degraded / down against thresholds, and emit a structured JSON health report a dashboard could scrape. By the end you own a single command that returns a ranked latency-and-health picture of a whole fleet. Real, runnable Python throughout.

Built step-by-step with [KhwajaLabs Build](https://khwajalabs.com).

## Stack
- Python
- TCP/IP
- sockets
- asyncio
- JSON
