import glob
import logging
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path

import requests

import bps.apply as bps
from bps.validate import CorruptFile

from source import config
from source import ips
from source import arguments

TIMEOUT = 10  # sec

PATCH_FILE_FORMATS = ["*.ips", "*.bps"]


def download_and_run(url: str):
    """
    Downloads a file from a URL, extracts it and runs a function with the extracted file.

    Args:
        url (str): The URL of the file to download.
    """
    try:
        file_name = os.path.basename(url)
        print(file_name)
        # todo: check if file is already in library (with download and patch again option)

        # download the file
        file_path = download_file(url)

        # extract the file
        extracted_path = unzip_file(file_path)

        # find the patch files
        patch_files = find_files_by_extensions(extracted_path, PATCH_FILE_FORMATS)

        # apply first found patch file
        # todo: if multiple, create browser to select which patch to apply
        if patch_files:
            try:
                patched_file = apply_patch(patch_files[0], "lol.sfc")
                run_patched_file(patched_file)
            except (CorruptFile, NotADirectoryError) as error:
                logging.error(error)
    except requests.exceptions.HTTPError as error:
        logging.error(error)


def download_file(file_url: str) -> Path:
    """
    Downloads a file from a URL and saves it to a temporary directory.

    Args:
        file_url (str): The URL of the file to download.

    Returns:
        Path: The path to the downloaded file.
    """
    # get filename from download URL
    file_name = os.path.basename(file_url)

    # save file in temp dir
    file_path = Path(os.path.join(tempfile.mkdtemp(), file_name))

    # download the file
    response = requests.get(file_url, timeout=TIMEOUT)

    # check if the download was successful
    if response.status_code == 200:
        # open the local file in binary write mode and write the content of the response to it
        with open(file_path, mode="wb") as file:
            file.write(response.content)

        logging.info("File downloaded and saved as %s", file_path)
        return file_path

    raise requests.exceptions.HTTPError(
        f'Failed to download "{file_name}". Status code: {response.status_code}'
    )


def unzip_file(zip_path: Path) -> Path:
    """
    Extracts a ZIP file to the same directory as the ZIP file.

    Args:
        zip_path (Path): The path to the ZIP file.

    Returns:
        Path: The path to the directory where the ZIP file was extracted.
    """
    # get path from ZIP file
    directory_path = os.path.dirname(zip_path)

    # read the ZIP file
    with zipfile.ZipFile(zip_path, mode="r") as zip_ref:
        # extract the zip in the same path as its stored in
        zip_ref.extractall(directory_path)

    logging.info("ZIP extracted to %s", directory_path)
    return Path(directory_path)


def find_files_by_extensions(directory: Path, file_extensions: list) -> list:
    """
    Search for files with specified extensions in a directory and its subdirectories.

    Args:
        directory (Path): The directory to search in.
        file_extensions (list): A list of file extensions to search for.

    Returns:
        list: A list of matching file paths.
    """
    matching_files = []
    for extension in file_extensions:
        matching_files.extend(
            glob.glob(os.path.join(directory, "**", extension), recursive=True)
        )

    logging.info(
        "Found %s files with extensions %s: %s",
        len(matching_files),
        file_extensions,
        matching_files,
    )
    return matching_files


def apply_patch(patch_path: Path, dest_file_name: str) -> Path:
    """
    Applies a patch file to a target file.

    Args:
        patch_path (Path): The path to the patch file.

    Returns:
        Path: The path to the patched file.
    """

    source_path = arguments.Arguments().get_sfc_path()

    lib_path = config.Config().get_library_path()
    if not lib_path.is_dir():
        raise NotADirectoryError(f"Library path '{lib_path}' is not a directory!")
    dest_path = lib_path.joinpath(dest_file_name)

    # IPS patches
    if str(patch_path).endswith(".ips"):
        success, msg = ips.apply_patch(source_path, patch_path, dest_path)
        if not success:
            raise CorruptFile(msg)

    # BPS patches
    elif str(patch_path).endswith(".bps"):
        patch_stream = open(patch_path, mode="rb")
        source_stream = open(source_path, mode="rb")
        dest_stream = open(dest_path, mode="wb")
        bps.apply_to_files(patch_stream, source_stream, dest_stream)

    logging.info(
        "Patched '%s' to '%s', saved as '%s'", patch_path, source_path, dest_path
    )
    return Path(dest_path)


def copy_patched_file_to_library(patched_file: Path) -> Path:
    """
    Copies a patched file to the library.

    Args:
        patched_file (Path): The path to the patched file.

    Returns:
        Path: The new path to the patched file.
    """
    return patched_file


def run_patched_file(file_path: Path):
    """
    Runs a patched file.

    Args:
        file_path (Path): The path to the patched file.
    """
    logging.info("Trying to run %s", file_path)
    try:
        subprocess.run([config.Config().get_launch_program_path(), file_path], check=True)
        logging.info("Launch program exited")
    except subprocess.CalledProcessError as error:
        logging.error(error)
