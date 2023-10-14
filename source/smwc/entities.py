from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from typing import List


class Difficulty(Enum):
    ANY = ("Any", None)  # Any difficulty allowed
    EASY = ("Standard: Easy", 104)
    NORMAL = ("Standard: Normal", 105)
    HARD = ("Standard: Hard", 106)
    VERY_HARD = ("Standard: Very Hard", 141)
    KAIZO_BEGINNER = ("Kaizo: Beginner", 196)
    KAIZO_INTERMEDIATE = ("Kaizo: Intermediate", 107)
    KAIZO_EXPERT = ("Kaizo: Expert", 197)
    TOOL_ASSISTED_KAIZO = ("Tool-Assisted: Kaizo", 124)
    TOOL_ASSISTED_PIT = ("Tool-Assisted: Pit", 125)
    MISC_TROLL = ("Misc.: Troll", 161)
    NA = ("N/A", None)  # For the "N/A" case


class SortBy(Enum):
    DATE = ("Date", "date")
    NAME = ("Name", "name")
    FEATURED = ("Featured", "featured")
    LENGTH = ("Length", "length")
    RATING = ("Rating", "rating")
    FILESIZE = ("Size", "filesize")
    DOWNLOADS = ("Downloads", "downloads")


@dataclass
class HackEntry:
    """This represent a table entry for a hack on SMW Central."""

    name: str
    date: datetime
    demo: bool
    featured: bool
    length: int
    difficulty: Difficulty
    author: str
    rating: float
    size: str
    download_count: int
    download_url: str


@dataclass
class PageList:
    """This represent a page list for other pages on SMW Central."""

    active_page: int
    pages: dict


@dataclass
class Page:
    hacks: List[HackEntry]
    page_list: PageList


def difficulty_string_to_enum(value: str) -> Difficulty:
    for difficulty_enum in Difficulty:
        if difficulty_enum.value[0] == value:
            return difficulty_enum

    raise ValueError(f"Cannot convert '{value}' to a Difficulty type")


def index_to_difficulty(index: int) -> Difficulty:
    difficultys = list(Difficulty)
    return difficultys[index]


def get_difficulty_names():
    names = [difficulty.value[0] for difficulty in Difficulty]
    return names[:-1]


def index_to_sort_by(index: int) -> SortBy:
    sort_bys = list(SortBy)
    return sort_bys[index]


def get_sort_by_names():
    names = [sort_by.value[0] for sort_by in SortBy]
    return names
