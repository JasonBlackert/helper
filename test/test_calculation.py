import os
import sys
import logging
import unittest

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

logging.basicConfig(filename='logs/unittest.log', level=logging.INFO)
logger = logging.getLogger(__name__)

from calculation import add, sub
from helper import whoami, elapsed

class TestAddFunction(unittest.TestCase):
    logger.info(f"Running {whoami()}...")
    @elapsed(out=logger.info)
    def test_add_positive_numbers(self):
        result = add((5, 7))
        self.assertEqual(result, 12)

    @elapsed(out=logger.info)
    def test_add_negative_numbers(self):
        result = add((-5, -7))
        self.assertEqual(result, -12)

    @elapsed(out=logger.info)
    def test_add_zero(self):
        result = add((0, 0))
        self.assertEqual(result, 0)


class TestSubtraction(unittest.TestCase):
    logger.info(f"Running {whoami()}...")
    @elapsed(out=logger.info)
    def test_sub_positive_numbers(self):
        result = sub((0, 0))
        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()
