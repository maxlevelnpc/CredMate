from PySide6.QtWidgets import QLineEdit


class Entry(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(32)
        self.setReadOnly(True)
        self.style_label = ("""
            QLineEdit {
                background-color: #2c3245;
                color: white;
                border: none;
                border-radius: 8px;
                text-align: center;
                font-size: 12px;
                padding: 8px 12px;
            }
        """)

        self.style_entry = ("""
            QLineEdit {
                background-color: #2c3245;
                color: white;
                border: 2px solid #3f7a99;
                border-radius: 8px;
                text-align: center;
                font-size: 12px;
                padding: 8px 12px;
            }
            QLineEdit:hover {
                background-color: #32394f;
            }
        """)
        self.setAsLabel()

    def setText(self, text):
        super().setText(text)
        self.setCursorPosition(0)

    def setAsLabel(self):
        self.setReadOnly(True)
        self.setStyleSheet(self.style_label)

    def setAsEntry(self):
        self.setReadOnly(False)
        self.setStyleSheet(self.style_entry)
