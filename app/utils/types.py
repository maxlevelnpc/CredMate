from typing import TypedDict, Literal, List, Union

class CredentialData(TypedDict):
    address: str
    username: str
    password: str
    modified: str  # Format: "YYYY-MM-DD HH:MM:SS"

# A hint for the sort options to avoid typos
SortType = Literal["az", "last_modified"]