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


def elect(peers: dict) -> tuple:
    """Returns (primary_hostname, fallback_hostname) from the peer table.
    Ranked by earliest start_time; hostname is the tiebreaker for ties."""
    ranked = sorted(peers.items(), key=lambda kv: (kv[1]["start_time"], kv[0]))
    primary = ranked[0][0] if len(ranked) >= 1 else None
    fallback = ranked[1][0] if len(ranked) >= 2 else None
    return primary, fallback

def init_command_set(obj: object= None):
    logger.debug(f"Initializing {obj} command set")
    if obj is None:
        return {}

    # Public callables
    command_set = {
        name: getattr(obj, name)
        for name in dir(obj)
        if callable(getattr(obj, name)) and not name.startswith("_")
    }

    undesired_methods = [ "test_method" ]
    for method in undesired_methods:
        command_set.pop(method, None)

    aliases = {name.replace("_", " "): fn for name, fn in command_set.items() if "_" in name}
    command_set.update(aliases)

    logger.debug(f"Populated command set = [ {command_set.keys()} ]")
    return command_set

def whoami():
    return inspect.stack()[1].function

@contextmanager
def acquire_lock(lock: Lock, timeout: float = DEFAULT_LOCK_TIMEOUT_S): # -> Iterator[bool]:
    """Wrapper method for acquiring and auto-releasing locks"""
    logger.debug(f"acquiring lock: {lock}")
    acquired = lock.acquire(timeout=timeout)

    try:
        yield acquired
    finally:
        if acquired:
            lock.release()

def retrieve_args(cast = float, argv=None, out=print): # -> tuple(float):
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
