import logging
import os
import tempfile
import zipfile
from pathlib import Path

import requests

TIMEOUT = 10  # sec


def download_file(file_url: str) -> Path:
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
    else:
        logging.warning(
            'Failed to download "%s". Status code: %s', file_name, response.status_code
        )


def unzip_file(zip_path: Path) -> Path:
    # get path from ZIP file
    directory_path = os.path.dirname(zip_path)

    # read the ZIP file
    with zipfile.ZipFile(zip_path, mode="r") as zip_ref:
        # extract the zip in the same path as its stored in
        zip_ref.extractall(directory_path)

    return Path(directory_path)
