"""
Author: Mirco Janisch

Date: 2023-10-03

Description: Command line argument parsing.
"""
import argparse
from pathlib import Path


class Arguments:
    """Singleton class for parsing command line arguments."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Arguments, cls).__new__(cls)
            cls._instance.init_singleton()
        return cls._instance

    def init_singleton(self):
        """Initialize singleton."""
        # pylint: disable=attribute-defined-outside-init
        self.args = self.parse_args()

    def parse_args(self) -> dict:
        """Parse command line arguments.

        Returns:
            dict: A dictionary of parsed arguments.
        """
        parser = argparse.ArgumentParser(description="SMW Central Browser")
        parser.add_argument("sfc_path", type=str, help="Path to the US SFC file")
        args = parser.parse_args()

        return {"sfc_path": args.sfc_path}

    def get_sfc_path(self) -> Path:
        """
        Get the path to the SFC file.

        Returns:
            str: The path to the SFC file.
        """
        return Path(self.args["sfc_path"])
