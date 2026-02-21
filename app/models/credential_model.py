from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import Signal

from app.core.types import CredentialData, SortType

if TYPE_CHECKING:
    from app.core.services import CredentialService


class CredentialModel:

    def __init__(self, service: CredentialService) -> None:
        self.service = service

        self.generic_credentials: list[CredentialData] = []
        self.misc_credentials: list[CredentialData] = []
    
    def is_exist(self, address: str) -> bool:
        all_creds = self.generic_credentials + self.misc_credentials
        for cred in all_creds:
            if cred.get("address").lower() == address.lower():
                return True
        return False

    def get_sorted_list(self, query: str = "", sort: SortType = SortType.AZ) -> list[CredentialData]:
        filtered = [c for c in self.generic_credentials if query.lower() in c['address'].lower()]
        if sort == SortType.AZ:
            filtered.sort(key=lambda c: c.get("address", "").lower())
        elif sort == SortType.Date:
            filtered.sort(key=lambda c: c.get("modified", ""), reverse=True)

        return filtered
    
    def load_credentials(self) -> Optional[str]:
        err, creds_data = self.service.get_windows_credentials()
        
        gen_creds, misc_creds = creds_data
        self.misc_credentials = misc_creds
        self.generic_credentials = gen_creds

        return err if err is not None else None

    def save_credential(self, cred_data: CredentialData, new):
        ok, msg = self.service.add_windows_credential(cred_data, new)
        if not ok:
            return False, msg

        # also update/add the credential in `generic_credentials` list
        address = cred_data.get("address")
        for cred in self.generic_credentials:
            if cred.get("address").lower() == address.lower():
                cred.update(cred_data)
                return True, f"Credential with address `{address}` updated."
        else:
            self.generic_credentials.append(cred_data)
            return True, f"New credential `{address}` added."
        
        return False, f"Failed to {'save new' if new else 'update'} credential."
    
    def delete_credential(self, address: str):
        ok, msg = self.service.delete_windows_credential(address)
        if not ok:
            return ok, msg

        # also delete the credential in `generic_credentials` list
        for cred in self.generic_credentials:
            if cred["address"] == address:
                self.generic_credentials.remove(cred)
                return True, f"Credential with address `{address}` deleted"
            
        return False, f"Failed to delete credential with address`{address}`"