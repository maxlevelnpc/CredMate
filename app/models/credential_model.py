from typing import Optional

class CredentialModel:
    def __init__(self, service):
        self.service = service

        self.generic_credentials: list = []
        self.misc_credentials: list = []

    def get_sorted_list(self, query="", sort="az"):
        """Model handles the logic of data processing"""
        filtered = [c for c in self.generic_credentials if query.lower() in c['address'].lower()]
        if sort == "az":
            filtered.sort(key=lambda c: c.get("address", "").lower())
        elif sort == "last_modified":
            filtered.sort(key=lambda c: c.get("modified", ""), reverse=True)

        return filtered