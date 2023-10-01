import argparse
import logging
import sys
import zlib
from pathlib import Path

SMW_CRC32 = "B19ED489"

LOG_LEVEL = logging.DEBUG

import source.gui.browser

def parse_args() -> dict:
    parser = argparse.ArgumentParser(description="Super Mario World Central Browser")
    parser.add_argument(
        "sfc_path", type=str, help="Path to the Super Mario World (USA) SFC file"
    )

    return parser.parse_args()


def crc32(file: Path) -> str:
    return "%X" % (zlib.crc32(open(file, "rb").read()) & 0xFFFFFFFF)


def main():
    logging.basicConfig(level=LOG_LEVEL)
    args = parse_args()

    if crc32(args.sfc_path) != SMW_CRC32:
        logging.critical("Given SFC has incorrect CRC32. Expected: %s", SMW_CRC32)
        sys.exit(1)


# output_path = "./output/"
# hacklist = Path(hack_path)

# if not hacklist.is_file():
#     browser = Chrome(options=opts)
#     hacklist = smwc.get_hack_list(browser)
#     with open("cache/hacks.json", "w") as fp:
#         json.dump(hacklist, fp)
#     browser.close()
#     print("Got the list! Run again to choose")
#     quit()
# else:
#     with open(hack_path) as f:
#         hacklist = json.load(f)

# smwc.set_hack_list(hacklist["hack_list"])
# hack = smwc.draw_table()
# download = smwc.download_hack(hack, temp_path)
# unzip = smwc.unzip_hack(download, temp_path)
# for f in unzip:
#     output_file = (
#         output_path + hack.get("title") + " (" + str(int(time.time())) + ").sfc"
#     )
#     if f.endswith(".bps"):
#         print("Patching " + hack.get("title") + " on to " + source_path)
#         smwc.apply_bps(f, source_path, output_file)
#         print("Outputted file to: " + output_file)
#     elif f.endswith(".ips"):
#         smwc.apply_ips(f, source_path, output_file)
#         print("Outputted file to: " + output_file)

if __name__ == "__main__":
    pass
