import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from inc.helper import retrieve_args

def add(addends: tuple(float) = (0,0)) -> float:
    return sum(addends)

def sub(minuend: tuple(float) = (0, 0)) -> float:
    return minuend[0] - sum(minuend[1:])

if __name__ == "__main__":
    sum = add(retrieve_args(type=float))
    print(f"{sum}")
