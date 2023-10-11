"""
Author:
    - written by Frederic Beaudet aka fbeaudet
    - modified by Mirco Janisch aka R3tr0BoiDX

Source: https://github.com/fbeaudet/ips.py

License: GPLv3

Version: 0.1

Description: Patches files using IPS patches.
"""
import gzip
import os
import shutil
import struct

FILE_LIMIT = 0x1000000  # 16MB
RECORD_LIMIT = 0x10000

PATCH_ASCII = bytes((0x50, 0x41, 0x54, 0x43, 0x48))
EOF_ASCII = bytes((0x45, 0x4F, 0x46))
EOF_INTEGER = 4542278


def apply_patch(original_file: str, patch_file: str, new_file: str):
    """Create an IPS patch.

    Args:
        original_file (str): Path to the original file.
        patch_file (str): Path to the patch file (.ips or .gzip).
        new_file (str): Where to write the new file.

    Returns:
        tuple: (bool, str) - Success, Message
    """

    # handling programmer errors
    assert isinstance(original_file, str), "'original_file' must be a string."
    assert isinstance(patch_file, str), "'patch_file' must be a string."
    assert isinstance(new_file, str), "'new_file must' be a string."

    # handling operational errors

    # original bytes
    try:
        original = open(original_file, "rb").read()
    except FileNotFoundError:
        return (False, f"There was a problem trying to read '{original_file}'.")

    # patch bytes
    try:
        if patch_file[-4:] == "gzip":
            patch = gzip.decompress(open(patch_file, "rb").read())
        else:
            patch = open(patch_file, "rb").read()
    except FileNotFoundError:
        return (False, f"There was a problem trying to read '{patch_file}'.")

    # buffer for writing
    try:
        new = open(new_file, "wb")  # file object
        os.write(new.fileno(), original)
    except FileNotFoundError:
        return (False, f"There was a problem trying to write to '{new_file}'.")

    # disk space
    directory = os.path.dirname(os.path.abspath(new_file))
    if directory == "":
        directory = "."

    if shutil.disk_usage(directory).free <= FILE_LIMIT:
        return (
            False,
            f"Not enough space for creating patch at specified path '{directory}'.",
        )

    # OK, tests passed

    # initial states
    a = 5
    while a < len(patch):
        # parse offset
        offset = struct.unpack(
            ">1i", struct.pack(">4B", 0, patch[a], patch[a + 1], patch[a + 2])
        )[0]

        # check if it's the end of the patch
        if offset == EOF_INTEGER:
            new.close()
            return (True, "Success")

        # parse size
        size = struct.unpack(
            ">1i", struct.pack(">4B", 0, 0, patch[a + 3], patch[a + 4])
        )[0]

        # write record content to file

        os.lseek(new.fileno(), offset, 0)

        if size != 0:
            # Normal record.
            # 3 bytes offset (not EOF_ASCII), 2 bytes size (not 0), x bytes data

            for x in range(size):
                os.write(new.fileno(), bytes([patch[a + 5 + x]]))

            # update loop address
            a += 5 + size

        else:
            # RLE record.
            # 3 bytes offset, 2 bytes size (0), 2 bytes times, 1 bytes data

            # parse the number of times to repeat the data
            times = struct.unpack(
                ">1i", struct.pack(">4B", 0, 0, patch[a + 5], patch[a + 6])
            )[0]

            for x in range(times):
                os.write(new.fileno(), bytes([patch[a + 7]]))

            # update loop address
            a += 8

    new.close()
    return (False, "Patch hadn't an EOF flag.")
