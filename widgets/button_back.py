from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize

from resources import icons  # noqa


class ButtonBack(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setIcon(QIcon(":/resources/left.png"))
        self.setIconSize(QSize(20, 20))
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #cbcccf;
                border: none;
                font-size: 26px;
                border-radius: 6px;
                text-align: left;
                outline: none;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
