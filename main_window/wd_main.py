from datetime import datetime
from typing import Literal, Optional

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from modules.credman_utils import credman_load, credman_write, credman_delete
from widgets.button_menu import ButtonMenu
from widgets.msgbox import MessageBox


class MainWindowLogic:
    def __init__(self, ui):
        self.ui = ui

        self._other_credentials: Optional[list] = None
        self.credential_list: Optional[list] = None
        self._last_sort: Optional[str] = None
        self._last_query: str = ""

    def setupLogic(self) -> None:
        creds, ot_creds = credman_load()
        self._other_credentials = ot_creds
        self.credential_list = creds

        self.ui.add_cred_btn.clicked.connect(self.on_add_new_credential)
        self.ui.copy_btn.clicked.connect(self.copy_password)
        self.ui.search_bar.app_settings.clicked.connect(lambda: self.switch_container(self.ui.settings_container))
        self.ui.search_bar.sort_modified.clicked.connect(lambda: self.on_apply_sort("last_modified"))
        self.ui.search_bar.sort_az.clicked.connect(lambda: self.on_apply_sort("az"))
        self.ui.search_bar.search_input.returnPressed.connect(lambda: self.update_credentials_buttons(self.ui.search_bar.search_input.text(), self._last_query))  # noqa
        self.ui.back_btn.clicked.connect(lambda: self.back_to_menu(self.ui.credential_container))
        self.ui.about_back_btn.clicked.connect(lambda: self.back_to_menu(self.ui.settings_container))
        self.ui.new_back_btn.clicked.connect(lambda: self.back_to_menu(self.ui.new_credential_container))

        self.ui.edit_btn.clicked.connect(self.enable_edit_mode)
        self.ui.cancel_del_btn.clicked.connect(self.delete_credential)
        self.ui.new_save_btn.clicked.connect(lambda: self.save_credential(new=True))

        self.ui.label_empty.setVisible(False)
        self.ui.credential_container.setVisible(False)
        self.ui.new_credential_container.setVisible(False)
        self.ui.settings_container.setVisible(False)

        self.load_credential_buttons()

    def load_credential_buttons(self, credentials=None, sort: Literal["az", "last_modified"] = "az"):
        creds = self.credential_list if credentials is None else credentials

        if sort == "az":
            creds.sort(key=lambda c: c.get("address", "").lower())
        elif sort == "last_modified":
            creds.sort(key=lambda c: c.get("modified", ""), reverse=True)

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

        self._last_sort = sort

    def _delete_credential_buttons(self):
        layout = self.ui.main_container_layout
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, ButtonMenu):
                widget.setParent(None)
                widget.deleteLater()

    def update_credentials_buttons(self, query, sort: Literal["az", "last_modified"] = "last_modified"):
        if query == self._last_query and sort == self._last_sort:
            return

        if query is not None or query != "" and sort != self._last_sort:
            self._delete_credential_buttons()

            # Filter credentials
            creds = [cred for cred in self.credential_list if query.lower() in cred.get("address", "").lower()]
        else:
            creds = self.credential_list

        self.load_credential_buttons(creds, sort)
        self._last_query = query

    def on_apply_sort(self, sort):
        if sort == self._last_sort:
            return

        self.update_credentials_buttons(self.ui.search_bar.search_input.text(), sort)

    def on_credential_click(self, cred):
        self.switch_container(self.ui.credential_container)

        if not self.ui.password.isReadOnly():
            self.on_cancel()

        address = cred.get("address", "NULL")
        username = cred.get("username", "Unknown")
        password = cred.get("password")
        modified = cred.get("modified")
        self.ui.address.setText(address)
        self.ui.user_name.setText(username)
        self.ui.password.setText(password)
        self.ui.modified_date.setText(modified)

    def on_add_new_credential(self):
        self.ui.new_address.clear()
        self.ui.new_user_name.clear()
        self.ui.new_password.clear()

        self.switch_container(self.ui.new_credential_container)
        self.ui.new_address.setFocus()

    def switch_container(self, curr_con):
        self.ui.main_container.moveContainer("hide_left")
        QTimer.singleShot(200, lambda: self.ui.scroll_area.setVisible(False))
        QTimer.singleShot(200, lambda: curr_con.setVisible(True))
        QTimer.singleShot(200, lambda: curr_con.moveContainer("show_right"))

    def back_to_menu(self, curr_con):
        curr_con.moveContainer("hide_right")
        QTimer.singleShot(200, lambda: curr_con.setVisible(False))
        QTimer.singleShot(200, lambda: self.ui.scroll_area.setVisible(True))
        QTimer.singleShot(200, lambda: self.ui.main_container.moveContainer("show_left"))

    def on_cancel(self):
        self.ui.password.setAsLabel()
        self.ui.password.setFixedHeight(32)
        self.ui.user_name.setAsLabel()
        self.ui.user_name.setFixedHeight(32)

        self.ui.edit_btn.setEditStyle()
        self.ui.edit_btn.setText("Edit")
        self.ui.edit_btn.clicked.disconnect()
        self.ui.edit_btn.clicked.connect(self.enable_edit_mode)

        self.ui.cancel_del_btn.setText("Delete")
        self.ui.cancel_del_btn.setDelStyle()
        self.ui.cancel_del_btn.clicked.disconnect()
        self.ui.cancel_del_btn.clicked.connect(self.delete_credential)

    def enable_edit_mode(self):
        self.ui.password.setAsEntry()
        self.ui.password.setFixedHeight(35)
        self.ui.user_name.setAsEntry()
        self.ui.user_name.setFixedHeight(35)
        self.ui.user_name.setFocus()

        self.ui.edit_btn.setText("Save")
        self.ui.edit_btn.clicked.disconnect()
        self.ui.edit_btn.clicked.connect(self.save_credential)
        self.ui.edit_btn.setSaveStyle()

        self.ui.cancel_del_btn.setText("Cancel")
        self.ui.cancel_del_btn.setEditStyle()
        self.ui.cancel_del_btn.clicked.disconnect()
        self.ui.cancel_del_btn.clicked.connect(self.on_cancel)

    def save_credential(self, new=False):
        msg = "Are you sure you want to add this new credential?" if new else "Are you sure you want to update this credential?"
        confirm = MessageBox("Confirm Action", msg)
        if confirm:
            address = self.ui.new_address.text() if new else self.ui.address.text()
            user_name = self.ui.new_user_name.text() if new else self.ui.user_name.text()
            password = self.ui.new_password.text() if new else self.ui.password.text()

            if new:
                all_creds = self.credential_list + self._other_credentials
                for cred in all_creds:
                    if cred.get("address").lower() == address.lower():
                        MessageBox(
                            "Duplicate Credential",
                            f"A credential with the address '{address}' already exists. Please use a unique name.",
                            info=True
                        )
                        return

            if not address or not user_name or not password:
                MessageBox("Error", "Field cannot be empty", True)
                return

            write_cred = credman_write(address, user_name, password, new)

            self.on_cancel()
            if new:
                self.credential_list.append({
                    "address": address,
                    "username": user_name,
                    "password": password,
                    "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                self._delete_credential_buttons()
                self.load_credential_buttons()

                if write_cred == "OK":
                    MessageBox("Success", "New credentials saved!", info=True)
                else:
                    MessageBox("Error", f"Failed to save new credential: {write_cred}", info=True)

                return

            if write_cred == "OK":
                MessageBox("Success", "Credentials updated!", info=True)
            else:
                MessageBox("Error", f"Failed to update credential: {write_cred}", info=True)

    def delete_credential(self):
        confirm = MessageBox(
            "Confirm Deletion",
            "Are you sure you want to delete this credential?"
        )

        if confirm:
            address = self.ui.address.text()
            del_cred = credman_delete(address)

            for cred in self.credential_list:
                if cred["address"] == address:
                    self.credential_list.remove(cred)

            self._delete_credential_buttons()
            self.load_credential_buttons()

            if del_cred == "OK":
                MessageBox("Success", "Credentials deleted!", info=True)
            else:
                MessageBox("Error", f"Failed to delete `{address}`: {del_cred}", info=True)

            self.back_to_menu(self.ui.credential_container)

    def copy_password(self):
        pwd = self.ui.password.text()
        QApplication.clipboard().setText(pwd)
