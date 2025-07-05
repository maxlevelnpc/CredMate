from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QFrame, QPushButton, QCompleter
from PySide6.QtGui import QPixmap, QGuiApplication, QIcon
from PySide6.QtCore import Qt, QSize, QStringListModel


class SearchBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)

        self.icon_label = QLabel()
        pixmap = QPixmap(":/app/resources/icons/search.png")
        pixmap.setDevicePixelRatio(QGuiApplication.primaryScreen().devicePixelRatio())
        pixmap = pixmap.scaled(
            20, 20,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.icon_label.setPixmap(pixmap)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search credentials...")

        self.sort_modified = QPushButton()
        self.sort_modified.setIcon(QIcon(":/app/resources/icons/sort_modified.png"))
        self.sort_modified.setObjectName("transButton")

        self.sort_az = QPushButton()
        self.sort_az.setIcon(QIcon(":/app/resources/icons/sort_az.png"))
        self.sort_az.setObjectName("transButton")

        self.app_settings = QPushButton()
        self.app_settings.setIcon(QIcon(":/app/resources/icons/settings.png"))
        self.app_settings.setIconSize(QSize(22, 22))
        self.app_settings.setObjectName("transButton")

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(0)
        btn_layout.addWidget(self.sort_modified)
        btn_layout.addWidget(self.sort_az)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.app_settings)

        layout = QHBoxLayout(self)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.search_input)
        layout.addLayout(btn_layout)

    def text(self):
        return self.search_input.text()

    def setSearchCompleter(self, addresses: list):
        completer = QCompleter()
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setModel(QStringListModel(addresses))
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.search_input.setCompleter(completer)
