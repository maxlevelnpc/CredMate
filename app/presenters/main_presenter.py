from __future__ import annotations
import os
from datetime import datetime
from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QLineEdit

from app.widgets.buttons import ButtonMenu
from app.widgets.msgbox import MessageBox
from app.utils.types import TypedDict, SortType

if TYPE_CHECKING:
    from app.views.main_view import MainView
    from app.models.credential_model import CredentialModel


class MainPresenter:
    def __init__(self, model: CredentialModel, ui: MainView):
        self.model = model
        self.ui = ui

        self._last_sort: str = ""
        self._last_query: str = ""

        self.setupLogic()

    def setupLogic(self) -> None:
        """connect signals and call initializer functions"""
        self.ui.setWindowTitle(f"Credential Vault ({os.getlogin()})")

        creds, ot_creds = self.model.service.get_credentials()
        self.model.misc_credentials = ot_creds
        self.model.generic_credentials = creds

        self.ui.add_cred_btn.clicked.connect(self.on_new_credential_click)
        self.ui.copy_btn.clicked.connect(self.ui.password.copy_password)
        self.ui.search_bar.app_settings.clicked.connect(lambda: self.ui.root_container.slideToIndex(3))
        self.ui.search_bar.sort_modified.clicked.connect(lambda: self.show_sorted_result("last_modified"))
        self.ui.search_bar.sort_az.clicked.connect(lambda: self.show_sorted_result("az"))
        self.ui.search_bar.search_input.returnPressed.connect(self.show_search_result)
        self.ui.back_btn.clicked.connect(self.back_to_menu)
        self.ui.about_back_btn.clicked.connect(self.back_to_menu)
        self.ui.new_back_btn.clicked.connect(self.back_to_menu)

        self.ui.edit_btn.clicked.connect(lambda: self.on_edit_mode(set_enable=True))
        self.ui.cancel_del_btn.clicked.connect(self.delete_credential)
        self.ui.new_save_btn.clicked.connect(lambda: self.save_credential(new=True))

        self.ui.label_empty.setVisible(False)
        self.ui.credential_container.setVisible(False)
        self.ui.new_credential_container.setVisible(False)
        self.ui.settings_container.setVisible(False)

        hk_pwd_visibility = QShortcut(QKeySequence("Ctrl+Shift+P"), self.ui)
        hk_pwd_visibility.activated.connect(self.password_visibility)

        self.display_credentials(init=True)
        self.set_search_completer()


    def set_search_completer(self) -> None:
        addresses = [cred["address"] for cred in self.model.generic_credentials]
        self.ui.search_bar.setSearchCompleter(addresses)

    @Slot()
    def password_visibility(self):
        n, p = QLineEdit.EchoMode.Normal, QLineEdit.EchoMode.Password
        pwd, pwd_new = self.ui.password, self.ui.new_password

        pwd.setEchoMode(n) if pwd.echoMode() == p else pwd.setEchoMode(p)
        pwd_new.setEchoMode(n) if pwd_new.echoMode() == p else pwd_new.setEchoMode(p)

    def _create_credential_buttons(self, credentials):
        for cred in credentials:
            address = cred.get("address", "Unknown")
            modified, _ = cred.get("modified").split(" ")
            btn = ButtonMenu(address, modified)
            btn.clicked.connect(lambda _, c=cred: self.on_credential_click(c))
            self.ui.main_container_layout.addWidget(btn)

    def _delete_credential_buttons(self) -> None:
        layout = self.ui.main_container_layout
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, ButtonMenu):
                widget.setParent(None)
                widget.deleteLater()

    def display_credentials(self, query="", sort: SortType = "az", init=False) -> None:
        filtered_creds = self.model.get_sorted_list(query, sort)

        if not init:
            if query == self._last_query and sort == self._last_sort:
                return
        
            self._delete_credential_buttons()

        if not filtered_creds:
            self.ui.label_empty.setVisible(True)
        else:
            self.ui.label_empty.setVisible(False)
            self._create_credential_buttons(filtered_creds)

    def show_sorted_result(self, sort):
        self.display_credentials(self._last_query, sort)

        self._last_sort = sort

    def show_search_result(self):
        query = self.ui.search_bar.text()
        self.display_credentials(query, self._last_sort)

        self._last_query = query


    @Slot()
    def save_credential(self, new=False) -> None:
        msg = "Are you sure you want to add this new credential?" if new else "Are you sure you want to update this credential?"
        confirm = MessageBox("Confirm Action", msg)
        if confirm:
            address = self.ui.new_address.text() if new else self.ui.address.text()
            user_name = self.ui.new_user_name.text() if new else self.ui.user_name.text()
            password = self.ui.new_password.text() if new else self.ui.password.text()

            if not address or not user_name or not password:
                MessageBox("Error", "Field cannot be empty!", info=True)
                return

            if new:
                # check for duplicate address before adding new credential.
                # also compare with other credentials (non Enterprise ↓)
                all_creds = self.model.generic_credentials + self.model.misc_credentials
                for cred in all_creds:
                    if cred.get("address").lower() == address.lower():
                        MessageBox(
                            "Duplicate Credential",
                            f"A credential with the address '{address}' already exists. Please use a unique name.",
                            info=True
                        )
                        return

            ok, error = self.model.service.add_credential(address, user_name, password, new)

            self.on_edit_mode(set_enable=False)

            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = {
                    "address": address,
                    "username": user_name,
                    "password": password,
                    "modified": date_now
                }

            if new:
                self.model.generic_credentials.append(new_data)
            else:
                for cred in self.model.generic_credentials:
                    if cred.get("address").lower() == address.lower():
                        cred.update(new_data)

            self._delete_credential_buttons()
            self.display_credentials(init=True)
            self.set_search_completer()

            if ok:
                MessageBox("Success", "New Credential Added!" if new else "Credential Updated!", info=True)
            else:
                MessageBox("Error", f"Failed to {'save new' if new else 'update'} credential: {error}", info=True)

            if not new:
                self.ui.modified_date.setText(date_now)

    @Slot()
    def delete_credential(self) -> None:
        confirm = MessageBox(
            "Confirm Deletion",
            "Are you sure you want to delete this credential?"
        )

        if confirm:
            address = self.ui.address.text()
            ok, error = self.model.service.delete_credential(address)

            for cred in self.model.generic_credentials:
                if cred["address"] == address:
                    self.model.generic_credentials.remove(cred)

            self._delete_credential_buttons()
            self.display_credentials(init=True)
            self.set_search_completer()

            if ok:
                MessageBox("Success", "Credentials deleted!", info=True)
            else:
                MessageBox("Error", f"Failed to delete `{address}`: {error}", info=True)

            self.back_to_menu()


    @Slot()
    def on_credential_click(self, cred) -> None:
        self.ui.root_container.slideToIndex(1)

        if not self.ui.password.isReadOnly():
            # call this in case if user previously on edit mode and go back to main menu without close it
            self.on_edit_mode(set_enable=False)

        address = cred.get("address", "NULL")
        username = cred.get("username", "Unknown")
        password = cred.get("password")
        modified = cred.get("modified")
        self.ui.address.setText(address)
        self.ui.user_name.setText(username)
        self.ui.password.setText(password)
        self.ui.modified_date.setText(modified)

    @Slot()
    def on_new_credential_click(self) -> None:
        self.ui.new_address.clear()
        self.ui.new_user_name.clear()
        self.ui.new_password.clear()

        self.ui.root_container.slideToIndex(2)
        self.ui.new_address.setFocus()

    @Slot()
    def back_to_menu(self, curr_con) -> None:
        self.ui.root_container.slideToIndex(0)

    def on_edit_mode(self, set_enable=True):
        self.ui.edit_mode(set_enable)

        if set_enable:
            self.ui.user_name.setFocus()
            self.ui.edit_btn.clicked.connect(self.save_credential)
            self.ui.cancel_del_btn.clicked.connect(lambda: self.on_edit_mode(set_enable=False))
        else:
            self.ui.cancel_del_btn.clicked.connect(self.delete_credential)
            self.ui.edit_btn.clicked.connect(lambda: self.on_edit_mode(set_enable=True))

