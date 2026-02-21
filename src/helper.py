import sys
import time
import inspect
import logging

from contextlib import contextmanager
from threading import Lock
from functools import wraps

logger = logging.getLogger(__name__)

DEFAULT_LOCK_TIMEOUT_S = 0.001 # 1 ms
ELAPSED_DECIMAL_PLACE = 5

def whoami():
    return inspect.stack()[1].function

@contextmanager
def acquire_lock(lock: Lock, timeout: float = DEFAULT_LOCK_TIMEOUT_S) -> Iterator[bool]:
    """Wrapper method for acquiring and auto-releasing locks"""
    logger.debug(f"acquiring lock: {lock}")
    acquired = lock.acquire(timeout=timeout)

    try:
        yield acquired
    finally:
        if acquired:
            lock.release()

def retrieve_args(cast = float, argv=None, out=print) -> tuple(float):
    try:
        if argv is None:
            argv = sys.argv
        arguments = tuple(cast(arg) for i, arg in enumerate(argv) if i > 0)
        out(f"[InputArguments]: {arguments}")
        return arguments
    except Exception as ue:
        out(f"[UnknwonException]: {ue}")

def elapsed(clock=time.time, out=print):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_s = clock()
            response = func(*args, **kwargs)

            delta = round(clock() - start_s, ELAPSED_DECIMAL_PLACE)
            
            out(f"\t[elapsed] {func.__name__} took {delta} seconds")
            return response
        return wrapper
    return decorator


@elapsed
def main():
    print(f"{retrieve_args()}")

if __name__ == "__main__":
    main()
