# Fleet Health & Latency Checks: Know Your Nodes in Milliseconds

A systems project that builds the operational health layer a latency-sensitive shop lives on. This is not a security port scanner — it is the diagnostic tool that answers "is the fleet healthy right now, and which node is slow?" Measures TCP connect latency with a socket and a clock, shows why p99 matters far more than the average for trading, computes percentiles honestly, resolves and times DNS, verifies the default gateway and routing, and checks that a service port is not just open but actually answering. Simultaneously checks out concurrently across many nodes with asyncio, classifies each node healthy / degraded / down against thresholds, and emits a structured JSON health report a dashboard could scrape. Owns a single command that returns a ranked latency-and-health picture of a whole fleet. Real, runnable Python throughout.

## Stack
- Python
- TCP/IP
- sockets
- asyncio
- JSON
