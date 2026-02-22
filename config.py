""" 
    Author: Jason E. Blackert

    config.py: "What is my purpose?"
    developer: "You act as a namespace for configurable variables."
    config.py: "Oh my god."
"""
    
import os
import sys
import json
import logging

from typing import Optional

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


def load_json(path: str = "configuration.json") -> Optional[dict]:
    """Serves as a helper method specifically for class Configuration
    for future modules to utilize it."""
    with open(path, "r") as file:
        return json.load(file)

class Configuration():
    """ Namespae to hold all configurable values """
    def __init__(self, configuration: Optional[dict] = None):
        if not configuration or not isinstance(configuration, dict):
            configuration = {}
        
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"Configuration(): {configuration}")
        # super().__init__(configuration=configuration)
        
        # Make objects from configuration.json
        if not configuration.get("nested_imports", False):
            for outer, inner in configuration.items():
                self.logger.debug(f"outer: {outer} inner: {inner}")
                setattr(self, outer, inner)
        else:
            # If nested dictionaries need to be imported instead
            for outer, inner in configuration.items():
                if isinstance(inner, dict):
                    for inner, value in inner.items():
                        self.logger.debug(f"inner: {inner} value: {value}")
                        setattr(self, inner, value)
                else:
                    self.logger.debug(f"outer: {outer} inner: {inner}")
                    setattr(self, outer, inner)
        

