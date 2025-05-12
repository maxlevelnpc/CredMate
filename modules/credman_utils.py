import datetime
from typing import Union

import pywintypes
import win32cred


def credman_load() -> Union[tuple, str]:
    """:returns: tuple with two list or return error message as string"""
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

            if cred.get("Persist") == win32cred.CRED_PERSIST_ENTERPRISE:
                credential_list.append({
                    "address": target,
                    "username": user,
                    "password": password,
                    "modified": modified.strftime("%Y-%m-%d %H:%M:%S") if modified else "Unknown"
                })
            else:
                other_credentials.append({
                    "address": target,
                    "username": user,
                    "password": password,
                    "modified": modified.strftime("%Y-%m-%d %H:%M:%S") if modified else "Unknown"
                })
        return credential_list, other_credentials

    except pywintypes.error as e:
        return str(e)


def credman_write(address: str, username: str, password: str, new=False) -> str:
    """:returns: string 'OK' if success, else error message"""
    if not new:
        # If updating, ensure the credential exists first.
        # CredRead will raise an error if the given address doesn't exist,
        # preventing accidental creation of a new credential.
        win32cred.CredRead(address, win32cred.CRED_TYPE_GENERIC)

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
        return "OK" if "Element not found" in str(e) else str(e)

    return "OK"


def credman_delete(address: str) -> str:
    """:returns: string 'OK' if success, else error message"""
    try:
        win32cred.CredDelete(address, win32cred.CRED_TYPE_GENERIC, 0)
        return "OK"
    except pywintypes.error as e:
        return str(e)
