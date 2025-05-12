from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QFrame, QPushButton
from PySide6.QtGui import QPixmap, QGuiApplication, QIcon
from PySide6.QtCore import Qt, QSize

from resources import icons  # noqa


class SearchBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.setStyleSheet("""
            QFrame {
                background-color: #262b3c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 10px;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                outline: none;
            }
        """)

        self.icon_label = QLabel()
        self.icon_label.setStyleSheet("background-color: transparent; border: none")
        pixmap = QPixmap(":/resources/search.png")
        pixmap.setDevicePixelRatio(QGuiApplication.primaryScreen().devicePixelRatio())
        pixmap = pixmap.scaled(
            20, 20,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.icon_label.setPixmap(pixmap)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search credentials...")
        self.search_input.setStyleSheet("background-color: transparent; border: none;")

        self.sort_modified = QPushButton()
        self.sort_modified.setIcon(QIcon(":/resources/sort_modified.png"))

        self.sort_az = QPushButton()
        self.sort_az.setIcon(QIcon(":/resources/sort_az.png"))

        self.app_settings = QPushButton()
        self.app_settings.setIcon(QIcon(":/resources/settings.png"))
        self.app_settings.setIconSize(QSize(22, 22))

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
