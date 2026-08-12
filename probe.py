import socket
import time

# Measure how long it takes to COMPLETE a TCP connect to host:port, in
# milliseconds. Returns the latency, or None if the connect failed/timed out.
def tcp_connect_ms(host: str, port: int, timeout: float = 1.0) -> float | None:
    # A monotonic clock never goes backwards and isn't affected by the system
    # clock being adjusted — the only correct choice for measuring a duration.
    start = time.perf_counter()
    try:
        # socket.create_connection does the full DNS + TCP handshake, then
        # closes when the `with` block exits.
        with socket.create_connection((host, port), timeout=timeout):
            pass
    except (OSError, socket.timeout):
        return None  # could not connect within the timeout
    elapsed = time.perf_counter() - start
    return elapsed * 1000.0  # seconds → milliseconds
