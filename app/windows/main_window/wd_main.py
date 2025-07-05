from datetime import datetime
from typing import Literal, Optional

from PySide6.QtCore import QTimer, Slot
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QLineEdit, QMainWindow

from app.modules.credmate_utils import credman_load, credman_write, credman_delete
from app.widgets.buttons import ButtonMenu
from app.widgets.msgbox import MessageBox


class MainWindowLogic:
    def __init__(self, main_window: QMainWindow, ui):
        self.main_wd = main_window
        self.ui = ui

        self.credential_list: Optional[list] = None
        self.other_credentials: Optional[list] = None
        self._last_sort: Optional[str] = None
        self._last_query: str = ""

    def setupLogic(self) -> None:
        """connect signals and call initializer functions"""
        creds, ot_creds = credman_load()
        self.other_credentials = ot_creds
        self.credential_list = creds

        self.ui.add_cred_btn.clicked.connect(self.on_new_credential_click)
        self.ui.copy_btn.clicked.connect(self.ui.password.copy_password)
        self.ui.search_bar.app_settings.clicked.connect(lambda: self.switch_container(self.ui.settings_container))
        self.ui.search_bar.sort_modified.clicked.connect(lambda: self.on_apply_sort("last_modified"))
        self.ui.search_bar.sort_az.clicked.connect(lambda: self.on_apply_sort("az"))
        self.ui.search_bar.search_input.returnPressed.connect(lambda: self.update_credentials_buttons(self.ui.search_bar.search_input.text(), self._last_query))  # noqa
        self.ui.back_btn.clicked.connect(lambda: self.back_to_menu(self.ui.credential_container))
        self.ui.about_back_btn.clicked.connect(lambda: self.back_to_menu(self.ui.settings_container))
        self.ui.new_back_btn.clicked.connect(lambda: self.back_to_menu(self.ui.new_credential_container))

        self.ui.edit_btn.clicked.connect(lambda: self.edit_mode(set_enable=True))
        self.ui.cancel_del_btn.clicked.connect(self.delete_credential)
        self.ui.new_save_btn.clicked.connect(lambda: self.save_credential(new=True))

        self.ui.label_empty.setVisible(False)
        self.ui.credential_container.setVisible(False)
        self.ui.new_credential_container.setVisible(False)
        self.ui.settings_container.setVisible(False)

        hk_pwd_visibility = QShortcut(QKeySequence("Ctrl+Shift+P"), self.main_wd)
        hk_pwd_visibility.activated.connect(self.password_visibility)

        self.load_credential_buttons()
        self.set_search_completer()

    def load_credential_buttons(self, credentials=None, sort: Literal["az", "last_modified"] = "az") -> None:
        """create buttons represent each credential address"""
        creds = self.credential_list if credentials is None else credentials

        if sort == "az":
            creds.sort(key=lambda c: c.get("address", "").lower())
        elif sort == "last_modified":
            creds.sort(key=lambda c: c.get("modified", ""), reverse=True)

        # create the buttons with address as button text
        # if user doesn't have any credential, show label with text "empty." instead
        if not creds:
            self.ui.label_empty.setVisible(True)
        else:
            self.ui.label_empty.setVisible(False)

            for cred in creds:
                address = cred.get("address", "Unknown")
                modified, _ = cred.get("modified").split(" ")
                btn = ButtonMenu(address, modified)
                btn.clicked.connect(lambda _, c=cred: self.on_credential_click(c))
                self.ui.main_container_layout.addWidget(btn)

        # store it for later checks, avoid unnecessary buttons recreation
        self._last_sort = sort

    def _delete_credential_buttons(self) -> None:
        layout = self.ui.main_container_layout
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, ButtonMenu):
                widget.setParent(None)
                widget.deleteLater()

    @Slot()
    def update_credentials_buttons(self, query, sort: Literal["az", "last_modified"] = "last_modified") -> None:
        """
        recreate buttons.
        """
        if query == self._last_query and sort == self._last_sort:
            return

        if query is not None or query != "" and sort != self._last_sort:
            self._delete_credential_buttons()
            # Filter credentials. new list contains addresses based on search query
            creds = [cred for cred in self.credential_list if query.lower() in cred.get("address", "").lower()]
        else:
            creds = self.credential_list

        self.load_credential_buttons(creds, sort)
        self._last_query = query

    @Slot()
    def on_apply_sort(self, sort) -> None:
        if sort == self._last_sort:
            return

        self.update_credentials_buttons(self.ui.search_bar.search_input.text(), sort)

    @Slot()
    def on_credential_click(self, cred) -> None:
        self.switch_container(self.ui.credential_container)

        if not self.ui.password.isReadOnly():
            # call this in case if user previously on edit mode and go back to main menu without close it
            self.edit_mode(set_enable=False)

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

        self.switch_container(self.ui.new_credential_container)
        self.ui.new_address.setFocus()

    @Slot()
    def switch_container(self, curr_con) -> None:
        self.ui.main_container.moveContainer("hide_left")
        QTimer.singleShot(200, lambda: self.ui.scroll_area.setVisible(False))
        QTimer.singleShot(200, lambda: curr_con.setVisible(True))
        QTimer.singleShot(200, lambda: curr_con.moveContainer("show_right"))

    @Slot()
    def back_to_menu(self, curr_con) -> None:
        curr_con.moveContainer("hide_right")
        QTimer.singleShot(200, lambda: curr_con.setVisible(False))
        QTimer.singleShot(200, lambda: self.ui.scroll_area.setVisible(True))
        QTimer.singleShot(200, lambda: self.ui.main_container.moveContainer("show_left"))
        QTimer.singleShot(200, lambda: self.password_visibility(hide=True))

    def edit_mode(self, set_enable=True):
        self.ui.password.updateStyle("edit_mode" if set_enable else "normal")
        self.ui.password.setFixedHeight(32)
        self.ui.password.setReadOnly(not set_enable)

        self.ui.user_name.updateStyle("edit_mode" if set_enable else "normal")
        self.ui.user_name.setFixedHeight(32)
        self.ui.user_name.setReadOnly(not set_enable)

        self.ui.edit_btn.setText("Save" if set_enable else "Edit")
        self.ui.edit_btn.updateStyle("save" if set_enable else "normal")
        self.ui.edit_btn.clicked.disconnect()

        self.ui.cancel_del_btn.setText("Cancel" if set_enable else "Delete")
        self.ui.cancel_del_btn.updateStyle("normal" if set_enable else "delete")
        self.ui.cancel_del_btn.clicked.disconnect()

        if set_enable:
            self.ui.user_name.setFocus()
            self.ui.edit_btn.clicked.connect(self.save_credential)
            self.ui.cancel_del_btn.clicked.connect(lambda: self.edit_mode(set_enable=False))
        else:
            self.ui.cancel_del_btn.clicked.connect(self.delete_credential)
            self.ui.edit_btn.clicked.connect(lambda: self.edit_mode(set_enable=True))

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
                all_creds = self.credential_list + self.other_credentials
                for cred in all_creds:
                    if cred.get("address").lower() == address.lower():
                        MessageBox(
                            "Duplicate Credential",
                            f"A credential with the address '{address}' already exists. Please use a unique name.",
                            info=True
                        )
                        return

            ok, error = credman_write(address, user_name, password, new)

            self.edit_mode(set_enable=False)

            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = {
                    "address": address,
                    "username": user_name,
                    "password": password,
                    "modified": date_now
                }

            if new:
                self.credential_list.append(new_data)
            else:
                for cred in self.credential_list:
                    if cred.get("address").lower() == address.lower():
                        cred.update(new_data)

            self._delete_credential_buttons()
            self.load_credential_buttons()
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
            ok, error = credman_delete(address)

            for cred in self.credential_list:
                if cred["address"] == address:
                    self.credential_list.remove(cred)

            self._delete_credential_buttons()
            self.load_credential_buttons()
            self.set_search_completer()

            if ok:
                MessageBox("Success", "Credentials deleted!", info=True)
            else:
                MessageBox("Error", f"Failed to delete `{address}`: {error}", info=True)

            self.back_to_menu(self.ui.credential_container)

    def set_search_completer(self) -> None:
        addresses = [cred["address"] for cred in self.credential_list]
        self.ui.search_bar.setSearchCompleter(addresses)

    @Slot()
    def password_visibility(self, hide=False):
        n, p = QLineEdit.EchoMode.Normal, QLineEdit.EchoMode.Password
        pwd, pwd_new = self.ui.password, self.ui.new_password

        if self.ui.credential_container.isVisible():
            pwd.setEchoMode(n) if pwd.echoMode() == p and not hide else pwd.setEchoMode(p)
        elif self.ui.new_credential_container.isVisible():
            pwd_new.setEchoMode(n) if pwd_new.echoMode() == p and not hide else pwd_new.setEchoMode(p)
