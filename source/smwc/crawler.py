import re
import urllib.request
import zipfile
from datetime import datetime
from os import listdir
from os.path import isdir, isfile, join
from typing import List
import logging

import requests
from bs4 import BeautifulSoup

from source.smwc.entry import Difficulty, HackEntry, difficulty_string_to_enum
import source.smwc.params as params

BASE_URL = "https://www.smwcentral.net/?p=section&s=smwhacks"
TIMEOUT = 10  # sec

YES_NO_DICT = {"yes": True, "no": False}
DATETIME_PATTERN = "%Y-%m-%dT%H:%M:%S"


def get_hack_list(
    url=BASE_URL,
    name: str = None,
    authors: List[str] = None,
    tags: List[str] = None,
    demo: bool = None,
    featured: bool = None,
    difficulty: Difficulty = None,
    description: str = None,
):
    filter_params = params.form_filter_params(
        name, authors, tags, demo, featured, difficulty, description
    )

    filter_params = "&".join(filter_params).replace(" ", "+")
    if filter_params:
        filter_params = "&" + filter_params

    url = url + filter_params

    # Get website data
    response = requests.get(url, timeout=TIMEOUT)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        list_content_div = soup.find("div", id="list-content")

        if not list_content_div:
            print("The div with id='list-content' was not found.")
        else:
            table_entries = list_content_div.find("table")

            if not table_entries:
                print("Table with entries was not found.")
            else:
                tbody = table_entries.find("tbody")

                if not tbody:
                    print("tbody not found in table.")
                else:
                    tr_entries = tbody.find_all("tr")

                    for tr_entry in tr_entries:
                        process_entry(tr_entry)


def process_entry(table_entry):
    td = table_entry.find_all("td")

    # Extract data from HTML
    name = td[0].find("a").get_text()
    date = datetime.strptime(td[0].find("time")["datetime"], DATETIME_PATTERN)
    demo = yes_no_to_bool(td[1].get_text())
    featured = yes_no_to_bool(td[2].get_text())
    length = extract_number(td[3].get_text())
    difficulty = td[4].get_text()
    author = (
        td[5].find("a").get_text() if td[5].find("a") is not None else td[5].get_text()
    )
    rating = float(td[6].get_text()) if td[6].get_text().isdigit() else None
    size = td[7].get_text()
    download_count = extract_number(td[8].find("span").get_text())
    download_url = td[8].find("a")["href"]

    # Convert difficulty to enum type
    try:
        difficulty = difficulty_string_to_enum(difficulty)
    except ValueError:
        logging.warning(
            "'%s' is not a valid difficulty. Using %s",
            difficulty,
            Difficulty.NA.value[0],
        )

    # Remove leading // if present
    if download_url.startswith("//"):
        download_url = download_url[2:]

    hack_entry = HackEntry(
        name,
        date,
        demo,
        featured,
        length,
        difficulty,
        author,
        rating,
        size,
        download_count,
        download_url,
    )

    # todo
    print(hack_entry)


def extract_number(text: str) -> int:
    return re.findall(r"\d+", text)[0]


def yes_no_to_bool(value: str) -> bool:
    result = YES_NO_DICT.get(value.lower(), None)
    return result if result is not None else False


def download_hack(h, path):
    url = h["download-link"]
    dlpath = path + "/_smwci.zip"

    opener = urllib.request.build_opener()
    opener.addheaders = [
        (
            "User-Agent",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36",
        )
    ]
    urllib.request.install_opener(opener)

    print("Downloading file from " + url)
    urllib.request.urlretrieve(url, dlpath)
    return dlpath


def unzip_hack(path, tmpdir):
    zip_ref = zipfile.ZipFile(path, "r")
    zip_ref.extractall(tmpdir)
    zip_ref.close()
    files = []
    for f in listdir(tmpdir):
        if isdir(join(tmpdir, f)):
            for fd in listdir(join(tmpdir, f)):
                files.append(join(tmpdir, f, fd))
        elif isfile(join(tmpdir, f)):
            files.append(join(tmpdir, f))
    return files


def apply_bps(patch_path, source_path, dest_path):
    # from bps.apply import apply_to_files
    # source_patch = open(patch_path, "rb")
    # source_rom = open(source_path, "rb")
    # dest_path = open(dest_path, "wb")
    # return apply_to_files(source_patch, source_rom, dest_path)
    pass


def apply_ips(patch_path, source_path, dest_path):
    # ips.applyPatch(source_path, patch_path, dest_path)
    pass
