import logging
import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

import source.smwc.params as params
from source.smwc.entry import Difficulty, HackEntry, difficulty_string_to_enum

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
) -> List[HackEntry]:
    # Get filter parameter string if any
    filter_params = params.form_filter_params(
        name, authors, tags, demo, featured, difficulty, description
    )
    filter_params = "&".join(filter_params).replace(" ", "+")
    if filter_params:
        # add leading '&' which is not added by join
        filter_params = "&" + filter_params

    # Add filter parameter to given URL if any
    url = url + filter_params

    # Get website data
    response = requests.get(url, timeout=TIMEOUT)

    hacks = []
    if response.status_code == 200:
        # Soup up HTML response
        soup = BeautifulSoup(response.text, "html.parser")

        # Navigate through HTML structure
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
                        # Extract and wrap information of table entry in a HackEntry object
                        hacks.append(process_entry(tr_entry))

    return hacks


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

    rating = float(td[6].get_text()) if is_float(td[6].get_text()) else None
    size = td[7].get_text()
    download_count = extract_number(td[8].find("span").get_text())
    download_url = td[8].find("a")["href"]

    # Convert difficulty to enum type
    try:
        difficulty = difficulty_string_to_enum(difficulty)
    except ValueError:
        logging.warning(
            "'%s' is not a valid difficulty or multiple. Using %s",
            difficulty,
            Difficulty.NA.value[0],
        )
        difficulty = Difficulty.NA

    # Add scheme if leading // is present
    if download_url.startswith("//"):
        download_url = "https:" + download_url

    return HackEntry(
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


def is_float(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False


def extract_number(text: str) -> int:
    return int(re.findall(r"\d+", text)[0])


def yes_no_to_bool(value: str) -> bool:
    result = YES_NO_DICT.get(value.lower(), None)
    return result if result is not None else False


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
