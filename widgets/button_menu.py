from PySide6.QtGui import QIcon, QFontMetrics, Qt
from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QSizePolicy

from resources import icons  # noqa


class ButtonMenu(QPushButton):
    def __init__(self, address, date):
        super().__init__()
        self.address_text = address
        self.init_elide_width = 250

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)  # Adjust margins as needed
        layout.setSpacing(8)

        self.icon_left = QLabel()
        self.icon_left.setPixmap(QIcon(":/resources/key.png").pixmap(18, 18))  # First Icon (Left)

        self.address_label = QLabel(self._elideText(address))  # Address with elided text
        self.address_label.setStyleSheet("color: white;")

        self.date_label = QLabel(date)
        self.date_label.setStyleSheet("color: #b9b9b9; font-size: 10px;")

        layout.addWidget(self.icon_left)
        layout.addWidget(self.address_label)
        layout.addStretch()
        layout.addWidget(self.date_label)

        self.setLayout(layout)

        self.setStyleSheet("""
            QPushButton {
                background-color: #262b3c;
                color: white;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 8px 12px;
                outline: none;
            }
            QPushButton:hover {
                background-color: #31364a;
            }
            QPushButton:pressed {
                background-color: #1f2333;
            }
            QLabel {
                background-color: transparent;
            }

            QLabel:hover {
                background-color: transparent;
            }
        """)

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
