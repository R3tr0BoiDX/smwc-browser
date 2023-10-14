import logging
import re
from datetime import datetime
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from source.smwc import params
from source.logger import LoggerManager
from source.smwc.entities import (
    Difficulty,
    HackEntry,
    SortBy,
    difficulty_string_to_enum,
    PageList,
    Page,
)

BASE_URL = "https://www.smwcentral.net"
TIMEOUT = 10  # sec

YES_NO_DICT = {"yes": True, "no": False}
DATETIME_PATTERN = "%Y-%m-%dT%H:%M:%S"


def get_page(
    url=None,
    name: str = None,
    authors: List[str] = None,
    tags: List[str] = None,
    demo: bool = None,
    featured: bool = None,
    difficulty: Difficulty = None,
    description: str = None,
    sort_by: SortBy = None,
    ascending: bool = None,
) -> Page:
    if url is None:
        # Get filter parameter string if any
        filter_params = params.form_filter_params(
            name,
            authors,
            tags,
            demo,
            featured,
            difficulty,
            description,
            sort_by,
            ascending,
        )

        # Add filter parameter to given URL if any
        url = BASE_URL + filter_params
    else:
        url = BASE_URL + url

    # Get website data
    response = requests.get(url, timeout=TIMEOUT)

    if response.status_code == 200:
        # Soup up HTML response
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract information from soup
        hacks = get_hacks(soup)
        page_list = get_page_list(soup)
        submissions, showing_from, showing_to = get_numbers(soup)

        return Page(hacks, page_list, submissions, showing_from, showing_to)

    LoggerManager().logger.error(
        "HTTP status code %s: Failed to get hacks from %s.",
        response.status_code,
        url,
    )


def get_hacks(soup: BeautifulSoup) -> List[HackEntry]:
    hacks = []
    # Navigate through HTML structure
    list_content_div = soup.find("div", id="list-content")
    if not list_content_div:
        LoggerManager().logger.error("The div with id='list-content' was not found.")
    else:
        table_entries = list_content_div.find("table")

        if not table_entries:
            LoggerManager().logger.error("Table with entries was not found.")
        else:
            tbody = table_entries.find("tbody")

            if not tbody:
                LoggerManager().logger.error("tbody not found in table.")
            else:
                tr_entries = tbody.find_all("tr")

                for tr_entry in tr_entries:
                    # Extract and wrap information of table entry in a HackEntry object
                    hacks.append(process_entry(tr_entry))

    return hacks


def get_page_list(soup: BeautifulSoup) -> PageList:
    pages = {}
    active_page = 0

    # Navigate through HTML structure
    ul_element = soup.find("ul", {"class": "page-list"})

    if not ul_element:
        LoggerManager().logger.debug(
            "The ul with class='page-list' was not found. Page might have no other pages."
        )
    else:
        # Collect all the li entries inside the ul element
        li_entries = ul_element.find_all("li")

        for li_entry in li_entries:
            # Get the active page number
            if "active" in li_entry.get("class", []):
                active_page = int(li_entry.text)
                continue
            elif "title" in li_entry.get("class", []):
                # Skip the entry with the 'title' class
                continue
            elif li_entry.select_one("select"):
                # Skip the entry with a child select tag
                continue
            else:
                # Get the a element inside the element
                a_element = li_entry.find("a")
                href = a_element["href"]
                page_number = int(a_element.text)
                pages[page_number] = href

    return PageList(active_page, pages)


def get_numbers(soup: BeautifulSoup) -> Tuple[int, int, int]:
    submissions = 0
    showing_from = 0
    showing_to = 0

    # Navigate through HTML structure

    # Find the div with id='bottom-menu'
    bottom_menu_div = soup.find("div", id="bottom-menu")

    if not bottom_menu_div:
        LoggerManager().logger.error("The div with id='bottom-menu' was not found.")
    else:
        # Find first p element
        p_element = bottom_menu_div.find("p")

        if not p_element:
            LoggerManager().logger.error(
                "The p element in the bottom menu was not found."
            )
        else:
            # Find all strong elements
            strong_elements = p_element.find_all("strong")

            if not strong_elements:
                LoggerManager().logger.error("No strong elements were found.")
            else:
                # Get the numbers from the strong elements
                submissions = int(strong_elements[0].text.replace(",", ""))
                showing_from = int(strong_elements[1].text)
                showing_to = int(strong_elements[2].text)

    return submissions, showing_from, showing_to


def process_entry(table_entry):
    td = table_entry.find_all("td")

    # Extract data from HTML
    name_and_link = td[0].find("a")
    name = name_and_link.get_text()
    # link = name_and_link["href"]  #  todo: for entry pages
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
