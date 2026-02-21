from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QFrame, QPushButton, QCompleter, QMenu
from PySide6.QtGui import QPixmap, QGuiApplication, QIcon, QAction
from PySide6.QtCore import Qt, QSize, QStringListModel


class SearchBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)

        self.icon_label = QLabel()
        pixmap = QPixmap(":/app/assets/icons/search.png")
        pixmap.setDevicePixelRatio(QGuiApplication.primaryScreen().devicePixelRatio())
        pixmap = pixmap.scaled(
            22, 22,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.icon_label.setPixmap(pixmap)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Search credentials...")


        self.sort_btn = QPushButton()
        self.sort_btn.setIcon(QIcon(":/app/assets/icons/filter.png"))
        self.sort_btn.setIconSize(QSize(16, 16))
        self.sort_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.sort_menu = QMenu()

        self.sort_modified = QAction()
        self.sort_modified.setText("Date")
        self.sort_modified.setIcon(QIcon(":/app/assets/icons/sort_modified.png"))

        self.sort_az = QAction()
        self.sort_az.setText("Name")
        self.sort_az.setIcon(QIcon(":/app/assets/icons/sort_az.png"))

        self.sort_menu.addAction(self.sort_modified)
        self.sort_menu.addAction(self.sort_az)

        self.sort_btn.setMenu(self.sort_menu)

        self.app_settings = QPushButton()
        self.app_settings.setIcon(QIcon(":/app/assets/icons/settings.png"))
        self.app_settings.setIconSize(QSize(22, 22))
        self.app_settings.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(0)
        btn_layout.addWidget(self.sort_btn)
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
