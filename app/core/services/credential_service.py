import datetime
import logging
from typing import Optional

import pywintypes
import win32cred

from app.core.types import CredentialData

log = logging.getLogger(__name__)


class CredentialService:
    def get_windows_credentials(self) -> tuple[Optional[str], tuple]:
        """:returns: tuple of; None or errpr message and a tuple with two list"""
        try:
            # create two list. other_credentials for later comparison
            other_credentials = []  # local computer, logon session etc.
            credential_list = []  # enterprise
            creds = win32cred.CredEnumerate(None, 0)
            for cred in creds:
                # only retrieve generic credentials
                if cred.get("Type") != win32cred.CRED_TYPE_GENERIC:
                    continue

                target = cred.get("TargetName", "")
                user = cred.get("UserName", "")

                password = ""
                blob = cred.get("CredentialBlob")
                if blob:
                    try:
                        password = blob.decode("utf-16")
                    except UnicodeDecodeError:
                        password = "[UNREADABLE]"

                timestamp = cred.get("LastWritten")
                modified = datetime.datetime.fromtimestamp(timestamp.timestamp()) if timestamp else None

                cred_list = credential_list if cred.get("Persist") == win32cred.CRED_PERSIST_ENTERPRISE else other_credentials
                cred_list.append({
                    "address": target,
                    "username": user,
                    "password": password,
                    "modified": modified.strftime("%Y-%m-%d %H:%M:%S") if modified else "Unknown"
                })

            return None, (credential_list, other_credentials)

        except pywintypes.error as e:
            log.error(str(e))
            return f"Failed to load credentials: {e}", ([], [])

    def add_windows_credential(self, cred_data: CredentialData, new=False) -> tuple[bool, Optional[str]]:
        """:return: (True, None) if successful, or (False, error message) on failure."""
        address = cred_data.get("address")
        username = cred_data.get("username")
        password = cred_data.get("password")
        
        if not new:
            # If updating, ensure the credential exists first.
            # CredRead will raise an error if the given address doesn't exist,
            # preventing accidental creation of a new credential.
            try:
                win32cred.CredRead(address, win32cred.CRED_TYPE_GENERIC)
            except pywintypes.error as e:
                if "Element not found" in str(e):
                    return False, f"Credential '{address}' not found. Cannot update non-existent entry."
                return False, f"Failed to read credential '{address}': {e}"

        credential = {
            'Type': win32cred.CRED_TYPE_GENERIC,
            'TargetName': address,
            'UserName': username,
            'CredentialBlob': password,
            'Persist': win32cred.CRED_PERSIST_ENTERPRISE,
        }
        try:
            win32cred.CredWrite(credential, 0)
        except pywintypes.error as e:
            log.error(str(e))
            return False, f"Failed to write credential '{address}': {e}"

        return True, None

    def delete_windows_credential(self, address: str) -> tuple[bool, Optional[str]]:
        """:return: (True, None) if successful, or (False, error message) on failure."""
        try:
            win32cred.CredDelete(address, win32cred.CRED_TYPE_GENERIC, 0)
            return True, None
        except pywintypes.error as e:
            log.error(str(e))
            return False, f"Failed to delete credential '{address}': {e}"

