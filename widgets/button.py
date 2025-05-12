from PySide6.QtWidgets import QPushButton


class Button(QPushButton):
    def __init__(self, text=None):
        super().__init__(text)
        self.style = ("""
            QPushButton {
                background-color: #262b3c;
                color: white;
                border: none;
                border-radius: 6px;
                text-align: center;
                padding: 8px 12px;
                outline: none;
            }
            QPushButton:hover {
                background-color: #3e4662;
            }
            QPushButton:pressed {
                background-color: #3e4662;
            }
        """)
        self.setEditStyle()

    def setEditStyle(self):
        self.setStyleSheet(self.style)

    def setSaveStyle(self):
        self.setStyleSheet(self.styleSheet() + """
            QPushButton {
                background-color: #3c9bcc;
            }
            QPushButton:hover {
                background-color: #54a3cc;
            }
        """)

    def setDelStyle(self):
        self.setStyleSheet(self.styleSheet() + """
            QPushButton {
                background-color: #ff4038;
            }
            QPushButton:hover {
                background-color: #ff4d38;
            }
        """)
