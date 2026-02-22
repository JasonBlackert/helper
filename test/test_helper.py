import os
import sys
import unittest
import logging

from threading import Lock

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from helper import whoami, retrieve_args, elapsed, acquire_lock

logging.basicConfig(filename='logs/unittest.log', level=logging.INFO)
logger = logging.getLogger(__name__)

shared_lock = Lock()

class TestAcquireLock(unittest.TestCase):
    logger.info(f"Running {whoami()}...")

    @elapsed(out=logger.info)
    def test_acquire_lock(self):
        with acquire_lock(shared_lock, timeout=0.5) as acquired:
            if not acquired:
                self.fail("Forcing failure in unittest")

        self.assertEqual(acquired, True)

class FakeOutput():
    def __init__(self):
        self.lines = []

    def __call__(self, msg):
        self.lines.append(str(msg))

class TestWhoAmI(unittest.TestCase):
    logger.info(f"Running {whoami()}...")
    @elapsed(out=logger.info)
    def test_whoami(self):
        self.assertEqual(whoami(), "test_whoami")

class TestRetrieveArgs(unittest.TestCase):
    logger.info(f"Running {whoami()}...")
    @elapsed(out=logger.info)
    def test_retrieve_args_good(self):
        fake_output = FakeOutput()
        argv = ["helper.py", "1.25", "2.5", "-3.5"]

        result = retrieve_args(cast=float, argv=argv, out=fake_output)

        self.assertEqual(result, (1.25, 2.5, -3.5))
        self.assertEqual(len(fake_output.lines), 1)
        self.assertTrue("[InputArguments]" in s for s in fake_output.lines)

    @elapsed(out=logger.info)
    def test_retrie_args_no_args(self):
        fake_output = FakeOutput()
        argv = ["helper.py"]
        result = retrieve_args(cast=float, argv=argv, out=fake_output)

        self.assertEqual(result, ())
        self.assertTrue(any("[InputArguments]:" in s for s in fake_output.lines))

    @elapsed(out=logger.info)
    def test_retrieve_args_bad_cast(self):
        fake_output = FakeOutput()
        argv = ["helper.py", "discover"]

        result = retrieve_args(cast=float, argv=argv, out=fake_output)

        self.assertIsNone(result)
        self.assertTrue(any("[UnknwonException]:" in s for s in fake_output.lines))

class TestElapsedDecorator(unittest.TestCase):
    logger.info(f"Running {whoami()}...")
    @elapsed(out=logger.info)
    def test_elapsed_returns_and_prints(self):
        fake_output = FakeOutput()

        fake_time_s = iter([100.0, 100.25])
        def fake_clock():
            return next(fake_time_s)

        @elapsed(clock=fake_clock, out=fake_output)
        def multiply(a, b):
            return a * b

        result = multiply(3, 4)
        self.assertEqual(result, 12)
        self.assertTrue(any("multiply took 0.25 seconds" in s for s in fake_output.lines))

if __name__ == "__main__":
    unittest.main()
