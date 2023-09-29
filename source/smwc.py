import re
import time
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime
from os import listdir
from os.path import isdir, isfile, join
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.smwcentral.net/?p=section&s=smwhacks"

YES_NO_DICT = {"yes": True, "no": False}
DATETIME_PATTERN = "%Y-%m-%dT%H:%M:%S"


@dataclass
class HackEntry:
    """This represent a table entry for a hack on SMW Central."""

    name: str
    date: datetime
    demo: bool
    featured: bool
    length: int
    hack_type: str
    author: str
    rating: float
    size: str
    download_count: int
    download_url: str


def get_hack_list(url=BASE_URL):
    # Get website data
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the first div called "list-content"
        list_content_div = soup.find("div", id="list-content")

        # Check if the element was found
        if list_content_div:
            # Find the first table element within the div
            entries_table = list_content_div.find("table")

            # Check if the table element was found
            if entries_table:
                tbody = entries_table.find("tbody")

                # Check if the <tbody> element was found
                if tbody:
                    entries = tbody.find_all("tr")

                    # Iterate over each entry
                    for entry in entries:
                        process_entry(entry)

                else:
                    print("tbody not found in table.")

            else:
                print("Table with entries was not found.")
        else:
            print("The div with id='list-content' was not found.")


def process_entry(table_entry):
    td = table_entry.find("tr").find_all("td")

    name = td[0].find("a").get_text()
    date = datetime.strptime(td[0].find("time")["datetime"], DATETIME_PATTERN)
    demo = yes_no_to_bool(td[1].get_text())
    featured = yes_no_to_bool(td[2].get_text())
    length = extract_number(td[3].get_text())
    hack_type = td[4].get_text()
    author = td[5].find("a").get_text()
    rating = float(td[6].get_text())
    size = td[7].get_text()
    download_count = extract_number(td[8].find("span").get_text())
    download_url = td[8].find("a")["href"]

    # Remove leading // if present
    if download_url.startswith("//"):
        download_url = download_url[2:]

    entry = HackEntry(
        name,
        date,
        demo,
        featured,
        length,
        hack_type,
        author,
        rating,
        size,
        download_count,
        download_url,
    )

    print(entry)


def extract_number(text: str) -> int:
    return re.findall(r"\d+", text)[0]


def yes_no_to_bool(value: str) -> bool:
    result = YES_NO_DICT.get(value.lower(), None)
    return result if result is not None else False


def old(url):
    print("Trying " + url)
    hackrows = browser.find_elements_by_xpath(
        "//div[@id='list_content']//table//tr[position()>1]"
    )

    for row in hackrows:
        firsttd = row.find_element_by_xpath(".//td[1]")
        infolink = firsttd.find_element_by_xpath(".//a").get_attribute("href")
        downloadlink = row.find_element_by_xpath(".//td[last()]//a").get_attribute(
            "href"
        )
        title = firsttd.find_element_by_xpath(".//a").text
        hack = {
            "id": parse_qs(urlparse(infolink).query).get("id")[0],
            "title": title,
            "added": datetime.strptime(
                firsttd.find_element_by_xpath(".//span//time").text,
                "%Y-%m-%d %I:%M:%S %p",
            ).strftime("%s"),
            "download-link": downloadlink,
            "detail-link": infolink,
        }
        print("Found " + title)
        hacklist.append(hack)

    nextpage = browser.find_element_by_xpath("//td[@id='menu2']//td[1]//a[last()]")
    try:
        nextpage = nextpage.get_attribute("href")
        print(
            "Found another page, trying page "
            + parse_qs(urlparse(nextpage).query).get("n")[0]
        )
        # return get_hack_list(browser, False, nextpage)
    except Exception as ex:
        print(ex)

    return {"updated": time.time(), "hack_list": hacklist}


def get_entry_from_title(title):
    hacklist = []
    for h in hacklist:
        if h["title"] == title:
            return h


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
    from bps.apply import apply_to_files

    source_patch = open(patch_path, "rb")
    source_rom = open(source_path, "rb")
    dest_path = open(dest_path, "wb")
    return apply_to_files(source_patch, source_rom, dest_path)


def apply_ips(patch_path, source_path, dest_path):
    # ips.applyPatch(source_path, patch_path, dest_path)
    pass


def get_title(h):
    return h.get("title")


def draw_table():
    global hacklist
    title = "Please select a hack:"
    # title, index = pick(hacklist, title, indicator="*", options_map_func=get_title)
    return title


if __name__ == "__main__":
    with open("example-entry.html", "r", encoding="utf-8") as file:
        file_content = file.read()

    soup = BeautifulSoup(file_content, "html.parser")
    process_entry(soup)
