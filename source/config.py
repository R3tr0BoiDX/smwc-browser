"""
Author: Mirco Janisch

Date: 2023-10-02

Description: Config file parsing.
"""
from pathlib import Path
import json

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
        self.config = self.read_json(Path(CONFIG_PATH))

    def read_json(self, config_file: Path) -> dict:
        """Read the config file.

        Args:
            config_file (Path): The path to the config JSON file.

        Returns:
            dict: The config as a dictionary.
        """
        # todo: add check if present
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
