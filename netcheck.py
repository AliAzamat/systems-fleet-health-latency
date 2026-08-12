import socket
import time

# Time how long DNS takes to resolve a name to an address. Slow DNS silently
# adds latency to every connect, so it's a health signal in its own right.
def resolve_ms(hostname: str, timeout: float = 1.0) -> float | None:
    socket.setdefaulttimeout(timeout)
    start = time.perf_counter()
    try:
        socket.gethostbyname(hostname)
    except socket.gaierror:
        return None  # resolution failed
    return (time.perf_counter() - start) * 1000.0

# Is the default gateway reachable on a TCP port (e.g. a router's management
# port)? A node that can't reach its gateway is islanded, however fast it is.
def gateway_reachable(gateway_ip: str, port: int = 179, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((gateway_ip, port), timeout=timeout):
            return True
    except OSError:
        return False

# An open port isn't enough — we want one that ANSWERS. Send a tiny probe and
# require some bytes back within the timeout. "Open but mute" is unhealthy.
def port_answers(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            s.sendall(b"PING\n")
            data = s.recv(1)         # expect at least one byte back
            return len(data) > 0
    except OSError:
        return False
