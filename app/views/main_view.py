from PySide6.QtCore import Qt, QSize, QTimer, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QMainWindow, QFormLayout, QScrollArea, QLabel, QLineEdit, QHBoxLayout, QWidget, 
    QGraphicsDropShadowEffect
)

from app.core.types import CredentialData
from app.widgets import Button, BackButton, Entry, SearchBar, SlideContainer


class MainView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUI()

    def setupUI(self) -> None:
        self.setWindowIcon(QIcon(":/app/assets/icons/icon.ico"))
        self.setMinimumSize(400, 400)

        central = QWidget(self)
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 10, 0, 10)

        self.root_container = SlideContainer()

        # fab. add to central
        self.back_btn = BackButton(central, ":/app/assets/icons/left.png", 40)
        self.back_btn.setOffset(20, 20)
        self.back_btn.setObjectName("backBtn")

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #   -- CREDENTIAL LIST AREA --

        self.cred_list_area = QScrollArea()
        self.cred_list_area.setWidgetResizable(True)
        self.cred_list_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.cred_list_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.cred_list_container = QWidget()
        self.cred_list_layout = QVBoxLayout(self.cred_list_container)
        self.cred_list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.cred_list_layout.setContentsMargins(10, 0, 10, 0)
        self.cred_list_layout.setSpacing(3)
        self.cred_list_area.setWidget(self.cred_list_container)

        searchbar_layout = QHBoxLayout()
        self.search_bar = SearchBar()
        self.search_bar.setObjectName("subContainer")
        self.add_cred_btn = Button()
        self.add_cred_btn.setIcon(QIcon(":/app/assets/icons/plus.png"))
        self.add_cred_btn.setIconSize(QSize(44, 44))
        searchbar_layout.addWidget(self.search_bar)
        searchbar_layout.addSpacing(2)
        searchbar_layout.addWidget(self.add_cred_btn)

        self.label_empty = QLabel()
        self.label_empty.setText("Empty.")

        self.cred_list_layout.addLayout(searchbar_layout)
        self.cred_list_layout.addSpacing(4)
        self.cred_list_layout.addWidget(self.label_empty, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #   -- CREDENTIAL DETAIL MENU --

        self.cred_info_container = QWidget()
        cred_info_layout = QVBoxLayout(self.cred_info_container)
        cred_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        detail_label = QLabel("Credential info")
        detail_label.setObjectName("titleLabel")

        self.cred_detail_container = QWidget()
        self.cred_detail_container.setObjectName("subContainer")
        cred_detail_layout = QVBoxLayout(self.cred_detail_container)
        cred_detail_layout.setContentsMargins(10, 10, 10, 10)
        cred_detail_layout.setSpacing(4)

        cred_form_layout = QFormLayout()
        self.address = Entry()
        self.user_name = Entry()
        pwd_layout = QHBoxLayout()
        self.password = Entry()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setToolTip("Press Ctrl+Shift+P to show/hide password.")
        self.copy_btn = Button()
        self.copy_btn.setObjectName("copyBtn")
        self.copy_btn.setFixedSize(32, 32)
        self.copy_btn.setIcon(QIcon(":/app/assets/icons/copy.png"))
        self.copy_btn.setIconSize(QSize(20, 20))
        pwd_layout.addWidget(self.password)
        pwd_layout.addWidget(self.copy_btn)
        self.modified_date = Entry()

        cred_form_layout.addRow("Network address", self.address)
        cred_form_layout.addRow("User name", self.user_name)
        cred_form_layout.addRow("Password", pwd_layout)
        cred_form_layout.addRow("Last modified", self.modified_date)

        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_btn = Button("Edit")
        self.edit_btn.setFixedSize(80, 35)
        self.cancel_del_btn = Button("Delete")
        self.cancel_del_btn.setFixedSize(80, 35)
        self.cancel_del_btn.updateStyle("delete")
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.cancel_del_btn)

        cred_detail_layout.addLayout(cred_form_layout)

        cred_info_layout.addSpacing(30)
        cred_info_layout.addWidget(detail_label, alignment=Qt.AlignmentFlag.AlignCenter)
        cred_info_layout.addWidget(self.cred_detail_container)
        cred_info_layout.addSpacing(10)
        cred_info_layout.addLayout(btn_layout)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #   -- CREDENTIAL CREATION MENU  --

        self.new_cred_container = QWidget()
        new_cred_layout = QVBoxLayout(self.new_cred_container)
        new_cred_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        info_label = QLabel("New generic credential")
        info_label.setObjectName("titleLabel")

        self.new_detail_container = QWidget()
        self.new_detail_container.setObjectName("subContainer")
        new_detail_layout = QVBoxLayout(self.new_detail_container)
        new_detail_layout.setContentsMargins(10, 10, 10, 10)
        new_detail_layout.setSpacing(4)

        new_form_layout = QFormLayout()
        self.new_address = Entry(False, "editMode")
        self.new_address.setFixedHeight(35)
        self.new_address.setPlaceholderText("Internet or network address")
        self.new_user_name = Entry(False, "editMode")
        self.new_user_name.setFixedHeight(35)
        self.new_user_name.setPlaceholderText("User name")
        self.new_password = Entry(False, "editMode")
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

        new_detail_layout.addLayout(new_form_layout)

        new_cred_layout.addSpacing(30)
        new_cred_layout.addWidget(info_label, alignment=Qt.AlignmentFlag.AlignCenter)
        new_cred_layout.addWidget(self.new_detail_container)
        new_cred_layout.addSpacing(10)
        new_cred_layout.addWidget(self.new_save_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #   -- SETTINGS / ABOUT PAGE --

        self.settings_container = QWidget()
        settings_layout = QVBoxLayout(self.settings_container)
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        app_about = QLabel()
        app_about.setObjectName("aboutLabel")
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

        settings_layout.addSpacing(60)
        settings_layout.addWidget(app_about, alignment=Qt.AlignmentFlag.AlignCenter)

        # /////////////////////////////////////////////////////////////////////////////////////////////////

        #  Add the four main containers to root container
        self.root_container.addWidget(self.cred_list_area)
        self.root_container.addWidget(self.cred_info_container)
        self.root_container.addWidget(self.new_cred_container)
        self.root_container.addWidget(self.settings_container)

        main_layout.addWidget(self.root_container)

    @Slot()
    def back_to_main_menu(self) -> None:
        self.root_container.slideToIndex(0)
        self.back_btn.setVisible(False)
    
    def show_back_btn(self) -> None:
        QTimer.singleShot(300, lambda: self.back_btn.setVisible(True))

    def update_credential_info(self, cred_data: CredentialData) -> None:
        self.address.setText(cred_data["address"])
        self.user_name.setText(cred_data["username"])
        self.password.setText(cred_data["password"])
        self.modified_date.setText(cred_data["modified"])  # type: ignore

    def edit_mode(self, enable: bool = True) -> None:
        self.password.updateStyle("editMode" if enable else "normalMode")
        self.password.setFixedHeight(32)
        self.password.setReadOnly(not enable)

        self.user_name.updateStyle("editMode" if enable else "normalMode")
        self.user_name.setFixedHeight(32)
        self.user_name.setReadOnly(not enable)

        self.edit_btn.setText("Save" if enable else "Edit")
        self.edit_btn.updateStyle("save" if enable else "normal")
        self.edit_btn.clicked.disconnect()

        self.cancel_del_btn.setText("Cancel" if enable else "Delete")
        self.cancel_del_btn.updateStyle("normal" if enable else "delete")
        self.cancel_del_btn.clicked.disconnect()
    
    @Slot()
    def password_visibility(self, hide: bool = False) -> None:
        n, p = QLineEdit.EchoMode.Normal, QLineEdit.EchoMode.Password
        pwd, pwd_new = self.password, self.new_password

        pwd.setEchoMode(n) if pwd.echoMode() == p and not hide else pwd.setEchoMode(p)
        pwd_new.setEchoMode(n) if pwd_new.echoMode() == p and not hide else pwd_new.setEchoMode(p)

    def apply_shadow(self, widget, color="#181818", blur=20, offset=(0, 0)):
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(blur)
        shadow.setXOffset(offset[0])
        shadow.setYOffset(offset[1])
        shadow.setColor(color)
        widget.setGraphicsEffect(shadow)