"""
Author: Mirco Janisch

Date: 2023-10-02

Description: Config file parsing.
"""
import json
import sys
from pathlib import Path

from source.logger import LoggerManager

CONFIG_PATH = "config.json"


class Config:
    """Singleton class for parsing and providing the config."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.init_singleton()
        return cls._instance

    def init_singleton(self):
        """Initialize singleton."""
        # pylint: disable=attribute-defined-outside-init
        try:
            self.config = self.read_json(Path(CONFIG_PATH))
        except FileNotFoundError as error:
            LoggerManager().logger.critical(error)
            sys.exit(1)

    def read_json(self, config_file: Path) -> dict:
        """Read the config file.

        Args:
            config_file (Path): The path to the config JSON file.

        Returns:
            dict: The config as a dictionary.

        Raises:
            FileNotFoundError: If the config file does not exist.
        """
        if not config_file.exists():
            raise FileNotFoundError(f"Config file {config_file} not found.")

        with open(config_file, mode="r", encoding="utf-8") as file:
            return json.load(file)

    def get_library_path(self) -> Path:
        """
        Get the path to the library directory.

        Returns:
            Path: The path to the library directory.
        """
        return Path(self.config["library_path"])

    def get_launch_program_path(self) -> Path:
        """
        Get the path to the launch program.

        Returns:
            Path: The path to the launch program.
        """
        return Path(self.config["launch_program"])

    def get_sfc_path(self) -> Path:
        """
        Get the path to the SFC file.

        Returns:
            str: The path to the SFC file.
        """
        return Path(self.config["sfc_path"])
