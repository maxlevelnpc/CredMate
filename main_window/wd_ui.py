import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QFormLayout, QHBoxLayout, QScrollArea, QLabel

from widgets.button import Button
from widgets.button_back import ButtonBack
from widgets.container import Container
from widgets.edit_entry import Entry
from widgets.search_bar import SearchBar


class MainWindowUI:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window

        self.scroll_area = None
        self.main_container = None
        self.main_container_layout = None
        self.credential_container = None
        self.new_credential_container = None
        self.settings_container = None

        self.search_bar = None
        self.add_cred_btn = None
        self.label_empty = None
        self.new_address = None
        self.new_user_name = None
        self.new_password = None
        self.new_save_btn = None
        self.new_back_btn = None
        self.back_btn = None
        self.address = None
        self.user_name = None
        self.password = None
        self.copy_btn = None
        self.persistence = None
        self.modified_date = None
        self.edit_btn = None
        self.cancel_del_btn = None
        self.about_back_btn = None

    def setupUi(self):
        self.main_window.setWindowTitle(f"Credential Vault ({os.getlogin()})")
        self.main_window.setWindowIcon(QIcon(":/resources/icon.ico"))
        self.main_window.setMinimumSize(400, 400)

        central_widget = Container(self.main_window)
        self.main_window.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 16px; 
            }
            
            QScrollBar::handle:vertical {
                background-color: #262b3c;
                min-height: 24px;
                border-radius: 4px;
                width: 8px;
                margin: 0 4px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #5e6a84;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        self.main_container = Container()
        self.main_container_layout = QVBoxLayout(self.main_container)
        self.main_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_container_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_area.setWidget(self.main_container)

        searchbar_layout = QHBoxLayout()
        self.search_bar = SearchBar()

        self.add_cred_btn = Button()
        self.add_cred_btn.setIcon(QIcon(":/resources/plus.png"))
        self.add_cred_btn.setIconSize(QSize(44, 44))

        searchbar_layout.addWidget(self.search_bar)
        searchbar_layout.addWidget(self.add_cred_btn)

        self.label_empty = QLabel()
        self.label_empty.setText("Empty.")
        self.label_empty.setStyleSheet("background: transparent; border: none; color: #b9b9b9; font-size: 16px;")

        self.main_container_layout.addLayout(searchbar_layout)
        self.main_container_layout.addSpacing(5)
        self.main_container_layout.addWidget(self.label_empty, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        self.credential_container = Container()
        credentials_layout = QVBoxLayout(self.credential_container)
        credentials_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.back_btn = ButtonBack(" Back")

        sub_credential_container = QWidget()  # noqa
        sub_credential_container.setStyleSheet("background: #262b3c; border: none; border-radius: 4px;")
        sub_credentials_layout = QVBoxLayout(sub_credential_container)
        sub_credentials_layout.setContentsMargins(10, 10, 10, 10)
        sub_credentials_layout.setSpacing(4)

        form_layout = QFormLayout()
        self.address = Entry()
        self.user_name = Entry()
        pwd_layout = QHBoxLayout()
        self.password = Entry()
        self.copy_btn = Button()
        self.copy_btn.setFixedSize(32, 32)
        self.copy_btn.setIcon(QIcon(":/resources/copy.png"))
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
        self.cancel_del_btn.setDelStyle()
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.cancel_del_btn)

        sub_credentials_layout.addLayout(form_layout)

        credentials_layout.addWidget(self.back_btn)
        credentials_layout.addSpacing(30)
        credentials_layout.addWidget(sub_credential_container)
        credentials_layout.addSpacing(10)
        credentials_layout.addLayout(btn_layout)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        self.new_credential_container = Container()
        new_credential_layout = QVBoxLayout(self.new_credential_container)
        new_credential_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.new_back_btn = ButtonBack(" Back")
        new_label = QLabel("New generic credential")
        new_label.setStyleSheet("font-size: 24px; color: #d8d8d8;")

        new_sub_credential_container = QWidget()  # noqa
        new_sub_credential_container.setStyleSheet("background: #262b3c; border: none; border-radius: 4px;")
        new_sub_credential_layout = QVBoxLayout(new_sub_credential_container)
        new_sub_credential_layout.setContentsMargins(10, 10, 10, 10)
        new_sub_credential_layout.setSpacing(4)

        new_form_layout = QFormLayout()
        self.new_address = Entry()
        self.new_address.setAsEntry()
        self.new_address.setFixedHeight(35)
        self.new_address.setPlaceholderText("Internet or network address")
        self.new_user_name = Entry()
        self.new_user_name.setFixedHeight(35)
        self.new_user_name.setAsEntry()
        self.new_user_name.setPlaceholderText("User name")
        self.new_password = Entry()
        self.new_password.setFixedHeight(35)
        self.new_password.setAsEntry()
        self.new_password.setPlaceholderText("Password")

        new_form_layout.addRow("Network address", self.new_address)
        new_form_layout.addRow("User name", self.new_user_name)
        new_form_layout.addRow("Password", self.new_password)

        self.new_save_btn = Button("Add")
        self.new_save_btn.setFixedSize(80, 35)

        new_sub_credential_layout.addLayout(new_form_layout)

        new_credential_layout.addWidget(self.new_back_btn)
        new_credential_layout.addSpacing(30)
        new_credential_layout.addWidget(new_label, alignment=Qt.AlignmentFlag.AlignCenter)
        new_credential_layout.addWidget(new_sub_credential_container)
        new_credential_layout.addSpacing(10)
        new_credential_layout.addWidget(self.new_save_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        self.settings_container = Container()
        settings_layout = QVBoxLayout(self.settings_container)
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.about_back_btn = ButtonBack(" Back")

        app_about = QLabel()
        app_about.setWordWrap(True)
        app_about.setText("""
            <h2 style="margin-bottom: 10px;">CredMate</h2>
            <p>
                CredMate helps you securely manage your <b>Generic Credentials</b> stored in Windows Credential Manager.<br><br>
                <b>[ i ]</b> This app only displays credentials marked with <b>Enterprise persistence</b>.<br><br>
                <i>by DODI — 2025.</i>
            </p>
        """)

        app_about.setStyleSheet("""
            QLabel {
                color: #cccccc;
                background-color: #1f2333;
                border-radius: 8px;
                padding: 12px 16px;
                max-width: 300px;
            }
        """)
        settings_layout.addWidget(self.about_back_btn)
        settings_layout.addSpacing(40)
        settings_layout.addWidget(app_about, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.credential_container)
        main_layout.addWidget(self.new_credential_container)
        main_layout.addWidget(self.settings_container)
