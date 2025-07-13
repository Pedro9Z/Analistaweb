import time

_LAST_REQUEST = 0.0
MAX_RPS = 5


def throttle() -> None:
    """Sleep if required to keep global request rate under MAX_RPS."""
    global _LAST_REQUEST
    delay = 1.0 / MAX_RPS
    now = time.time()
    elapsed = now - _LAST_REQUEST
    if elapsed < delay:
        time.sleep(delay - elapsed)
    _LAST_REQUEST = time.time()
