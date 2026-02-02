import os
from typing import Literal

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QWidget, QMainWindow, QFormLayout,
    QScrollArea, QLabel, QLineEdit, QHBoxLayout, QPushButton
)

from app.widgets.buttons import Button
from app.widgets.container import SlideContainer
from app.widgets.edit_entry import Entry
from app.widgets.search_bar import SearchBar


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUI()

    def setupUI(self):
        self.setWindowIcon(QIcon(":/app/resources/icons/icon.ico"))
        self.setMinimumSize(400, 400)
        self.setWindowOpacity(0.97)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.root_container = SlideContainer()

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #   -- MAIN CREDENTIAL LIST AREA --

        # Scroll area to hold the credential list
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Main container inside the scroll area
        self.main_container = QWidget()
        self.main_container_layout = QVBoxLayout(self.main_container)
        self.main_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_container_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_area.setWidget(self.main_container)

        searchbar_layout = QHBoxLayout()
        self.search_bar = SearchBar()

        self.add_cred_btn = Button()
        self.add_cred_btn.setIcon(QIcon(":/app/resources/icons/plus.png"))
        self.add_cred_btn.setIconSize(QSize(44, 44))

        searchbar_layout.addWidget(self.search_bar)
        searchbar_layout.addWidget(self.add_cred_btn)

        self.label_empty = QLabel()
        self.label_empty.setText("Empty.")
        self.label_empty.setObjectName("transLabel")

        self.main_container_layout.addLayout(searchbar_layout)
        self.main_container_layout.addSpacing(5)
        self.main_container_layout.addWidget(self.label_empty, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #   -- CREDENTIAL DETAIL PAGE --

        # Container to show selected credential information
        self.credential_container = QWidget()
        credential_layout = QVBoxLayout(self.credential_container)
        credential_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.back_btn = QPushButton(" Back")
        self.back_btn.setIcon(QIcon(":/app/resources/icons/left.png"))
        self.back_btn.setIconSize(QSize(20, 20))
        self.back_btn.setObjectName("backButton")

        sub_credential_container = QWidget()
        sub_credential_layout = QVBoxLayout(sub_credential_container)
        sub_credential_layout.setContentsMargins(10, 10, 10, 10)
        sub_credential_layout.setSpacing(4)

        form_layout = QFormLayout()
        self.address = Entry()
        self.user_name = Entry()
        pwd_layout = QHBoxLayout()
        self.password = Entry()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setToolTip("Press Ctrl+Shift+P to show/hide password.")
        self.copy_btn = Button()
        self.copy_btn.setFixedSize(32, 32)
        self.copy_btn.setIcon(QIcon(":/app/resources/icons/copy.png"))
        self.copy_btn.setIconSize(QSize(20, 20))
        pwd_layout.addWidget(self.password)
        pwd_layout.addWidget(self.copy_btn)
        self.modified_date = Entry()

        form_layout.addRow("Network address", self.address)
        form_layout.addRow("User name", self.user_name)
        form_layout.addRow("Password", pwd_layout)
        form_layout.addRow("Last modified", self.modified_date)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_btn = Button("Edit")
        self.edit_btn.setFixedSize(80, 35)
        self.cancel_del_btn = Button("Delete")
        self.cancel_del_btn.setFixedSize(80, 35)
        self.cancel_del_btn.updateStyle("delete")
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.cancel_del_btn)

        sub_credential_layout.addLayout(form_layout)

        credential_layout.addWidget(self.back_btn)
        credential_layout.addSpacing(30)
        credential_layout.addWidget(sub_credential_container)
        credential_layout.addSpacing(10)
        credential_layout.addLayout(btn_layout)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #   -- NEW CREDENTIAL CREATION PAGE  --

        self.new_credential_container = QWidget()
        new_credential_layout = QVBoxLayout(self.new_credential_container)
        new_credential_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.new_back_btn = QPushButton(" Back")
        self.new_back_btn.setIcon(QIcon(":/app/resources/icons/left.png"))
        self.new_back_btn.setIconSize(QSize(20, 20))
        self.new_back_btn.setObjectName("backButton")

        new_label = QLabel("New generic credential")
        new_label.setObjectName("titleLabel")

        new_sub_credential_container = QWidget()
        new_sub_credential_layout = QVBoxLayout(new_sub_credential_container)
        new_sub_credential_layout.setContentsMargins(10, 10, 10, 10)
        new_sub_credential_layout.setSpacing(4)

        new_form_layout = QFormLayout()
        self.new_address = Entry(False, "edit_mode")
        self.new_address.setFixedHeight(35)
        self.new_address.setPlaceholderText("Internet or network address")
        self.new_user_name = Entry(False, "edit_mode")
        self.new_user_name.setFixedHeight(35)
        self.new_user_name.setPlaceholderText("User name")
        self.new_password = Entry(False, "edit_mode")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setFixedHeight(35)
        self.new_password.setPlaceholderText("Password")
        self.password.setToolTip("Press Ctrl+Shift+P to show/hide password.")

        new_form_layout.addRow("Network address", self.new_address)
        new_form_layout.addRow("User name", self.new_user_name)
        new_form_layout.addRow("Password", self.new_password)

        self.new_save_btn = Button("Add")
        self.new_save_btn.setFixedSize(80, 35)
        self.new_save_btn.updateStyle("save")

        new_sub_credential_layout.addLayout(new_form_layout)

        new_credential_layout.addWidget(self.new_back_btn)
        new_credential_layout.addSpacing(30)
        new_credential_layout.addWidget(new_label, alignment=Qt.AlignmentFlag.AlignCenter)
        new_credential_layout.addWidget(new_sub_credential_container)
        new_credential_layout.addSpacing(10)
        new_credential_layout.addWidget(self.new_save_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #   -- SETTINGS / ABOUT PAGE --

        self.settings_container = QWidget()
        settings_layout = QVBoxLayout(self.settings_container)
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.about_back_btn = QPushButton(" Back")
        self.about_back_btn.setIcon(QIcon(":/app/resources/icons/left.png"))
        self.about_back_btn.setIconSize(QSize(20, 20))
        self.about_back_btn.setObjectName("backButton")

        app_about = QLabel()
        app_about.setObjectName("appAbout")
        settings_layout.addWidget(app_about)
        app_about.setWordWrap(True)
        app_about.setText("""
            <h2 style="margin-bottom: 10px;">CredMate</h2>
            <p>
                CredMate helps you securely manage your <b>Generic Credentials</b> stored in Windows Credential Manager.<br><br>
                <b>[ i ]</b> This app only displays credentials marked with <b>Enterprise persistence</b>.<br><br>
                <i>by DODI — 2025.</i>
            </p>
            <p></p>
        """)

        settings_layout.addWidget(self.about_back_btn)
        settings_layout.addSpacing(40)
        settings_layout.addWidget(app_about, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #  Add the four main containers to main layout
        self.root_container.addWidget(self.scroll_area)
        self.root_container.addWidget(self.credential_container)
        self.root_container.addWidget(self.new_credential_container)
        self.root_container.addWidget(self.settings_container)

        main_layout.addWidget(self.root_container)

    def set_credential_info(self):
        pass

    def edit_mode(self, set_enable=True):
        self.password.updateStyle("edit_mode" if set_enable else "normal")
        self.password.setFixedHeight(32)
        self.password.setReadOnly(not set_enable)

        self.user_name.updateStyle("edit_mode" if set_enable else "normal")
        self.user_name.setFixedHeight(32)
        self.user_name.setReadOnly(not set_enable)

        self.edit_btn.setText("Save" if set_enable else "Edit")
        self.edit_btn.updateStyle("save" if set_enable else "normal")
        self.edit_btn.clicked.disconnect()

        self.cancel_del_btn.setText("Cancel" if set_enable else "Delete")
        self.cancel_del_btn.updateStyle("normal" if set_enable else "delete")
        self.cancel_del_btn.clicked.disconnect()