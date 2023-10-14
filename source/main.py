"""Main entry point for the application."""
import logging
import sys
import zlib
from pathlib import Path

from source import arguments, config, logger
from source.gui import core

SMW_CRC32 = "B19ED489"


logging.basicConfig(level=logger.DEFAULT_LOG_LEVEL)
logger.LoggerManager()  # init logger
config.Config()  # init config
arguments.Arguments()  # init arguments


def main():
    """Main entry point for the application."""
    conf = config.Config()

    if conf.get_sfc_path() is None:
        logging.critical("No SFC path given!")
        sys.exit(1)

    if conf.get_sfc_path().exists() is False:
        logging.critical("Given SFC does not exist!")
        sys.exit(1)

    if conf.get_sfc_path().is_file() is False:
        logging.critical("Given SFC is not a file!")
        sys.exit(1)

    if crc32(conf.get_sfc_path()) != SMW_CRC32:
        logging.critical("Given SFC has incorrect CRC32. Expected: %s", SMW_CRC32)
        sys.exit(1)

    core.run()
    sys.exit()


def crc32(file: Path) -> str:
    """Calculate the CRC32 of a file.

    Args:
        file (Path): The path to the file.

    Returns:
        str: The CRC32 of the file.
    """
    # pylint: disable=consider-using-f-string
    return "%X" % (zlib.crc32(open(file, "rb").read()) & 0xFFFFFFFF)


if __name__ == "__main__":
    main()
