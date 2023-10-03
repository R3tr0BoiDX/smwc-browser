"""Main entry point for the application."""
import logging
import sys
import zlib
from pathlib import Path

from source import arguments, config
from source.gui import browser

SMW_CRC32 = "B19ED489"

LOG_LEVEL = logging.DEBUG

logging.basicConfig(level=LOG_LEVEL)
arguments.Arguments()  # init arguments
config.Config()  # init config


def main():
    """Main entry point for the application."""
    logging.basicConfig(level=LOG_LEVEL)
    args = arguments.Arguments()

    if crc32(args.get_sfc_path()) != SMW_CRC32:
        logging.critical("Given SFC has incorrect CRC32. Expected: %s", SMW_CRC32)
        sys.exit(1)

    browser.run()


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
