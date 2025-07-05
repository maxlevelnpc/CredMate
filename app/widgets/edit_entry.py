from typing import Literal

from PySide6.QtWidgets import QLineEdit, QApplication


class Entry(QLineEdit):
    def __init__(self, read_only=True, style: Literal["normal", "edit_mode"] = "normal"):
        super().__init__()

        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(32)
        self.setReadOnly(read_only)
        self.setObjectName("editEntry")
        self.updateStyle(style)

    def copy_password(self) -> None:
        QApplication.clipboard().setText(self.text())

    def setText(self, text):
        super().setText(text)
        self.setCursorPosition(0)

    def updateStyle(self, style: Literal["normal", "edit_mode"]):
        self.setProperty("style", style)
        self.style().unpolish(self)
        self.style().polish(self)
