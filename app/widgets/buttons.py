from typing import Literal

from PySide6.QtGui import QIcon, QFontMetrics, Qt
from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QSizePolicy


class Button(QPushButton):
    def __init__(self, text=None):
        super().__init__(text)
        self.setObjectName("appButton")
        self.updateStyle("normal")

    def updateStyle(self, style: Literal["normal", "save", "delete"]):
        self.setProperty("style", style)
        self.style().unpolish(self)
        self.style().polish(self)


class ButtonMenu(QPushButton):
    def __init__(self, address, date):
        super().__init__()
        self.address_text = address
        self.init_elide_width = 250

        self.setFixedHeight(35)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setObjectName("menuButton")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 4, 4)

        self.icon_left = QLabel()
        self.icon_left.setObjectName("transLabel")
        self.icon_left.setPixmap(QIcon(":/app/resources/icons/key.png").pixmap(14, 14))

        self.address_label = QLabel(self._elideText(address))
        self.address_label.setObjectName("addressLabel")

        self.date_label = QLabel(date)
        self.date_label.setObjectName("dateLabel")

        layout.addWidget(self.icon_left)
        layout.addWidget(self.address_label)
        layout.addStretch()
        layout.addWidget(self.date_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust max width dynamically based on new width
        max_width = max(50, self.width() - 150)  # Reserve space for icon and date
        self.address_label.setText(self._elideText(self.address_text, max_width))

    def _elideText(self, text, width=None):
        if width is None:
            width = self.init_elide_width
        fm = QFontMetrics(self.font())
        return fm.elidedText(text, Qt.TextElideMode.ElideRight, width)
