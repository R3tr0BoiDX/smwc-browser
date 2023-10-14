"""
Author: Mirco Janisch

Date: 2023-10-03

Description: Command line argument parsing.
"""
import argparse

from source.logger import LoggerManager
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
            description=f"{LONG_NAME} command line arguments - R3tr0BoiDX (c) 2023",
            add_help=True,
        )

        # dont start in fullscreen
        parser.add_argument(
            "-f",
            "--no-fullscreen",
            action="store_true",
            help=f"Don't start the {LONG_NAME} in fullscreen mode",
            default=False,
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
            "no_fullscreen": args.no_fullscreen,
            "no_launch": args.no_launch,
        }

    def get_no_fullscreen(self) -> bool:
        """
        Get the fullscreen argument.

        Returns:
            bool: The fullscreen argument.
        """
        try:
            return self.args["no_fullscreen"]
        except KeyError:
            return False

    def get_no_launch(self) -> bool:
        """
        If the program should not be launched after patching.

        Returns:
            bool: The no launch argument.
        """
        try:
            return self.args["no_launch"]
        except KeyError:
            return False
