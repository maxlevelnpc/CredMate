from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox

from resources import icons  # noqa


def MessageBox(title="Title", message="", info=False):
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(":/resources/icon.ico"))
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    if info:
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    else:
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: #1a2031;
            color: #d8dee9;
            font-size: 12px;
            border: none;
        }
        QPushButton {
            background-color: #262b3c;
            color: white;
            border: none;
            border-radius: 6px;
            text-align: center;
            padding: 8px 12px;
        }
        QPushButton:hover {
            background-color: #3e4662;
        }
    """)

    result = msg_box.exec()

    return result == QMessageBox.StandardButton.Yes

