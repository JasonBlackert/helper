""" 
    config.py: "What is my purpose?"
    developer: "You act as a namespace for configurable variables."
    config.py: "Oh my god."
"""
    
import os
import sys

from typing import Optional

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


class Configuration():
    """ Namespae to hold all configurable values """
    def __init__(self, configuration: Optional[dict] = None):
        if not configuration or not isinstance(configuration, dict):
            configuration = {}

        # super().__init__(configuration=configuration)

        # Make objects from configuration.json
        for outer, inner in configuration.items():
            if isinstance(inner, dict):
                for inner, value in inner.items():
                    setattr(self, inner, value)
            else:
                setattr(self, outer, inner)

