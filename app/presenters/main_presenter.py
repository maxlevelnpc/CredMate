from __future__ import annotations
import os
from datetime import datetime
from typing import TYPE_CHECKING
import logging

from PySide6.QtCore import Slot
from PySide6.QtGui import QKeySequence, QShortcut

from app.widgets import MenuButton, MessageBox
from app.core.types import SortType, CredentialData

if TYPE_CHECKING:
    from app.views import MainView
    from app.models import CredentialModel

log = logging.getLogger(__name__)


class MainPresenter:
    def __init__(self, model: CredentialModel, ui: MainView) -> None:
        self.model = model
        self.ui = ui

        self._last_sort: SortType = SortType.AZ
        self._last_query: str = ""

        self.setupPresenter()
        

    def setupPresenter(self) -> None:

        # APP SHORTCUTS
        HKEY_pwd_visibility = QShortcut(QKeySequence("Ctrl+Shift+P"), self.ui)
        HKEY_pwd_visibility.activated.connect(self.ui.password_visibility)

        # Load Windows Credentials before evrything else
        self.model.load_credentials()

        # Connect signals
        self.ui.add_cred_btn.clicked.connect(self.on_new_credential_click)
        self.ui.copy_btn.clicked.connect(self.ui.password.copy_password)
        self.ui.search_bar.app_settings.clicked.connect(self.open_settings)
        self.ui.search_bar.sort_modified.triggered.connect(lambda: self.show_sorted_result(SortType.Date))
        self.ui.search_bar.sort_az.triggered.connect(lambda: self.show_sorted_result(SortType.AZ))
        self.ui.search_bar.search_input.returnPressed.connect(self.show_search_result)
        self.ui.edit_btn.clicked.connect(lambda: self.on_edit_mode(set_enable=True))
        self.ui.cancel_del_btn.clicked.connect(self.on_delete_credential)
        self.ui.new_save_btn.clicked.connect(lambda: self.on_save_credential(new=True))
        self.ui.back_btn.clicked.connect(self.ui.back_to_main_menu)

        # Set widgets visibvility
        self.ui.label_empty.setVisible(False)
        self.ui.cred_info_container.setVisible(False)
        self.ui.new_cred_container.setVisible(False)
        self.ui.settings_container.setVisible(False)
        self.ui.back_btn.setVisible(False)

        # Call initializer functions
        self.set_window_title()
        self.display_credentials(query_and_sort_check=False, delete_buttons=False)
        self.update_search_completer()

        self.ui.apply_shadow(self.ui.search_bar)
        self.ui.apply_shadow(self.ui.add_cred_btn)
        self.ui.apply_shadow(self.ui.cred_detail_container)
        self.ui.apply_shadow(self.ui.new_detail_container)

        self.ui.apply_shadow(self.ui.back_btn)
        self.ui.apply_shadow(self.ui.edit_btn)
        self.ui.apply_shadow(self.ui.new_save_btn)
        self.ui.apply_shadow(self.ui.cancel_del_btn)

    def set_window_title(self) -> None:
        title = os.getlogin()
        creds = len(self.model.generic_credentials)
        self.ui.setWindowTitle(f"CREDMATE — {title} ({creds})")

    def update_search_completer(self) -> None:
        """
        Add search completer for the searchbar with address names
        """
        addresses = [cred["address"] for cred in self.model.generic_credentials]
        self.ui.search_bar.setSearchCompleter(addresses)
        log.debug("Search completer updated. ")

    @Slot()
    def open_settings(self) -> None:
        self.ui.root_container.slideToIndex(3)
        self.ui.show_back_btn()

    @Slot(dict)
    def on_credential_click(self, credential: CredentialData) -> None:
        """
        Show Detail Menu
        :param cred: Specific credential data to show
        """
        # Hide password in case user previously show it without hide it back
        self.ui.password_visibility(hide=True)
        self.ui.root_container.slideToIndex(1)

        if not self.ui.password.isReadOnly():
            # Disable edit mode in case if user previously on edit mode and go back to main menu without close it
            self.on_edit_mode(set_enable=False)

        self.ui.update_credential_info(credential)
        self.ui.show_back_btn()

    @Slot()
    def on_new_credential_click(self) -> None:
        """
        Open Creation Menu
        """
        self.ui.password_visibility(hide=True)
        self.ui.new_address.clear()
        self.ui.new_user_name.clear()
        self.ui.new_password.clear()

        self.ui.root_container.slideToIndex(2)
        self.ui.new_address.setFocus()

        self.ui.show_back_btn()

    @Slot(bool)
    def on_edit_mode(self, set_enable: bool = True) -> None:
        """
        Update Edit and Delete buttons behaviour
        :param set_enable: wether to set to normal or edit mode
        """
        self.ui.edit_mode(set_enable)

        if set_enable:
            self.ui.user_name.setFocus()
            self.ui.edit_btn.clicked.connect(self.on_save_credential)
            self.ui.cancel_del_btn.clicked.connect(lambda: self.on_edit_mode(set_enable=False))
        else:
            self.ui.cancel_del_btn.clicked.connect(self.on_delete_credential)
            self.ui.edit_btn.clicked.connect(lambda: self.on_edit_mode(set_enable=True))

    def _create_credential_buttons(self, credentials: list[CredentialData]) -> None:
        for cred in credentials:
            address = cred.get("address", "Unknown")
            modified, _ = cred.get("modified").split(" ")
            btn = MenuButton(address, modified)
            btn.clicked.connect(lambda _, c=cred: self.on_credential_click(c))
            self.ui.cred_list_layout.addWidget(btn)

        log.debug("Buttons created.")

    def _delete_credential_buttons(self) -> None:
        layout = self.ui.cred_list_layout
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, MenuButton):
                widget.setParent(None)
                widget.deleteLater()
        
        log.debug("Buttons deleted.")

    def display_credentials(
            self, 
            query: str = "", 
            sort: SortType = SortType.AZ, 
            query_and_sort_check: bool = True, 
            delete_buttons: bool = True
        ) -> None:
        """
        Create credential buttons based on specified query and sort them. Empty string query mean get all
        
        :param query: Show credentials contains this query. Empty string query mean get all
        :param sort: Sort type
        :param query_and_sort_check: To avoid unecesary button creation. Check if query and sort equal to its last value.
        :param delete_buttons: Wether to delete all previous buttons before recreate them back
        """
        filtered_creds = self.model.get_sorted_list(query, sort)

        if query_and_sort_check:
            log.debug(f"(1/6) Checking query and sort...")
            log.debug(f"(2/6) Specified query: {query}\n+ (3/6) Last query: {self._last_query}")
            log.debug(f"(4/6) Specified sort: {sort}\n+ (5/6) Last sort: {self._last_sort}")
            if query == self._last_query and sort == self._last_sort:
                log.debug("(6/6) Query and sort are the same with its last value. Buttons creation CANCELED!\n")
                return
            
            log.debug(f"(6/6) Query and sort are not the same with its last value. Continue buttons creation with specified query `{query}`, and apply sort `{sort}`\n")
        
        if delete_buttons:
            log.debug("(1/1) Deleting buttons...\n")
            self._delete_credential_buttons()

        if not filtered_creds:
            self.ui.label_empty.setVisible(True)
        else:
            self.ui.label_empty.setVisible(False)
            log.debug("(1/1) Creating buttons...\n")
            self._create_credential_buttons(filtered_creds)

    @Slot()
    def show_sorted_result(self, sort: SortType) -> None:
        """Show credential based on specified sort type"""
        self.display_credentials(self._last_query, sort)
        self._last_sort = sort

    @Slot()
    def show_search_result(self) -> None:
        """Show credential based on specified search query"""
        query = self.ui.search_bar.text()
        self.display_credentials(query, self._last_sort)
        self._last_query = query

    @Slot(bool)
    def on_save_credential(self, new: bool = False) -> None:
        """
        Update existing credential in Windows Credentials or add new one.
        :param new: True to add new credential, False to update exisiting one
        """
        address = self.ui.new_address.text() if new else self.ui.address.text()
        username = self.ui.new_user_name.text() if new else self.ui.user_name.text()
        password = self.ui.new_password.text() if new else self.ui.password.text()

        if not (address and username and password):
            MessageBox("Error", "Field cannot be empty!")
            return
    
        confirm = MessageBox(
            "Confirm Action", 
            "Are you sure you want to add this new credential?" if new else 
            "Are you sure you want to update this credential?",
            False
        )

        if not confirm:
            return

        if new:
            # check for duplicate address before adding new credential.
            is_exist = self.model.is_exist(address)
            if is_exist:
                MessageBox(
                    "Duplicate Credential",
                    f"A credential with the address '{address}' already exists. Please use a unique name."
                )
                return

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cred_data: CredentialData = {
            "address": address, 
            "username": username,
            "password": password,
            "modified": date_now
        }

        ok, msg = self.model.save_credential(cred_data, new)
        if not ok:
            MessageBox("Error", msg)
            return


        self.ui.modified_date.setText(date_now)

        self.display_credentials(sort=self._last_sort, query_and_sort_check=False)
        self.update_search_completer()
        self.on_edit_mode(set_enable=False)
        self.set_window_title()

        MessageBox("Success", msg)

    @Slot()
    def on_delete_credential(self) -> None:
        """
        Delete creedential in Windows Credentials        
        """
        confirm = MessageBox(
            "Confirm Deletion",
            "Are you sure you want to delete this credential?",
            False
        )

        if not confirm:
            return

        # delete credential
        address = self.ui.address.text()
        ok, msg = self.model.delete_credential(address)
        if not ok:
            MessageBox("Error", msg)
            return
    
        self.display_credentials(sort=self._last_sort, query_and_sort_check=False)
        self.update_search_completer()
        self.set_window_title()

        MessageBox("Success", msg)

        self.ui.back_to_main_menu()
