from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
