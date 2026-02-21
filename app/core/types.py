from typing import NotRequired, TypedDict
from enum import Enum, auto


class CredentialData(TypedDict):
    address: str
    username: str
    password: str
    modified: NotRequired[str]  # "YYYY-MM-DD HH:MM:SS"


class SortType(Enum):
    """
    AZ: Sort alphabetically (A to Z).
    Date: Sort by last modified date.
    """
    AZ = auto()
    Date = auto()