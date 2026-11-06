"""Windows-only stand-in for fcntl, for scripts/ratelimit_en.py. Add this folder to PYTHONPATH on Windows.
flock() is a no-op, so the rate limit is not shared between processes: run one network script at a time.
Do not use on Linux. The repository's own source is left unmodified."""
LOCK_EX = 2
LOCK_UN = 8
def flock(fd, operation):
    return None
