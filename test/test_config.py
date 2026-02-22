import os
import sys
import unittest
import logging

from threading import Lock

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from helper import elapsed, whoami
from config import Configuration, load_json

CONFIGURATION_PATH = "share/configuration.json"
configuration = load_json(CONFIGURATION_PATH)

logging.basicConfig(filename='logs/unittest.log', level=logging.INFO)
logger = logging.getLogger(__name__)


class TestConfiguration(unittest.TestCase):
    logger.info(f"Running {whoami()}...")

    @elapsed(out=logger.info)
    def test_load_json_typing(self):
        result = load_json(CONFIGURATION_PATH)
        self.assertEqual(type(result), dict)

    @elapsed(out=logger.info)
    def test_load_json_import(self):
        result = load_json(CONFIGURATION_PATH).get("unittest", "invalid")
        self.assertEqual(result, "DO_NOT_CHANGE")

    def test_config_setattr(self):
        config = Configuration(load_json(CONFIGURATION_PATH))
        self.assertEqual(config.unittest, "DO_NOT_CHANGE")

if __name__ == "__main__":
    unittest.main()
