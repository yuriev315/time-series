"""Cross-process per-host rate limiter.

Several processes (search helpers run by different workers, metadata and
download scripts) may hit the same host at once. Each call takes an exclusive
flock on a per-host file holding the last request time, sleeps until the
minimum interval has passed, then records the new time. Holding the lock while
sleeping serialises all callers.
"""
import fcntl
import os
import time

LOCK_DIR = os.environ.get("TSL_LOCK_DIR", "/tmp/tsl_ratelimit")


def wait(host, interval):
    os.makedirs(LOCK_DIR, exist_ok=True)
    path = os.path.join(LOCK_DIR, host.replace(":", "_").replace("/", "_"))
    with open(path, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        raw = f.read().strip()
        last = float(raw) if raw else 0.0
        delay = interval - (time.time() - last)
        if delay > 0:
            time.sleep(delay)
        f.seek(0)
        f.truncate()
        f.write(str(time.time()))
        f.flush()
