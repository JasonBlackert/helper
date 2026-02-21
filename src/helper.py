import sys
import time
import inspect

from threading import Lock
from functools import wraps

ELAPSED_DECIMAL_PLACE = 5

def whoami():
    return inspect.stack()[1].function

def acquire(lock: Lock, timeout=0.5):
    print(f"acquiring lock: {lock}")

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
