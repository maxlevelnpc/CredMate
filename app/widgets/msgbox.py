from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox


def MessageBox(title="Title", message="", info=False):
    msg_box = QMessageBox()
    msg_box.setWindowIcon(QIcon(":/app/resources/icons/icon.ico"))
    msg_box.setWindowTitle(title)
    msg_box.setText(message)

    if info:
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    else:
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    result = msg_box.exec()

    return result == QMessageBox.StandardButton.Yes

