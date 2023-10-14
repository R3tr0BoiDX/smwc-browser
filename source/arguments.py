"""
Author: Mirco Janisch

Date: 2023-10-03

Description: Command line argument parsing.
"""
import argparse
from pathlib import Path

from source.product_name import LONG_NAME


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
        parser = argparse.ArgumentParser(
            description=f"{LONG_NAME} command line arguments"
        )

        # argument for sfc path
        parser.add_argument(
            "-s",
            "--sfc-path",
            type=str,
            help="Path to the US SFC file",
            required=True,
        )

        # fullscreen argument
        parser.add_argument(
            "-f",
            "--fullscreen",
            action="store_true",
            help=f"Start {LONG_NAME} in fullscreen mode",
        )

        # dont launch program after patching
        parser.add_argument(
            "-l",
            "--no-launch",
            action="store_true",
            help=(
                "Don't launch the patched file using the program defined in the configuration file "
                "once patching is complete. If no program is defined, no program will be launched anyway."
            ),
            default=False,
        )

        args = parser.parse_args()

        return {
            "sfc_path": args.sfc_path,
            "fullscreen": args.fullscreen,
            "no_launch": args.no_launch,
        }

    def get_sfc_path(self) -> Path:
        """
        Get the path to the SFC file.

        Returns:
            str: The path to the SFC file.
        """
        return Path(self.args["sfc_path"])

    def get_fullscreen(self) -> bool:
        """
        Get the fullscreen argument.

        Returns:
            bool: The fullscreen argument.
        """
        return self.args["fullscreen"]

    def get_no_launch(self) -> bool:
        """
        If the program should not be launched after patching.

        Returns:
            bool: The no launch argument.
        """
        return self.args["no_launch"]
