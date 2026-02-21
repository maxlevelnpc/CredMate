from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox


def MessageBox(title: str, message: str, info: bool = True) -> bool:
    """
    Show a simple message box.

    Parameters:
        box_type (str): "info" for information, "ask" for Yes/No question.
        message (str): The message text to display.
        title (str): Optional window title.
    
    Returns:
        bool: For "ask", True if Yes clicked, False if No.
              For "info", always returns False.
    """
    m = QMessageBox()
    m.setWindowIcon(QIcon(":/app/assets/icons/icon.ico"))
    m.setWindowTitle(title)
    m.setText(message)

    if info:
        m.setIcon(QMessageBox.Icon.Information)
        m.setStandardButtons(QMessageBox.StandardButton.Ok)
        m.exec()
        return False

    else:
        m.setIcon(QMessageBox.Icon.Question)
        m.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        result = m.exec()
        return result == QMessageBox.StandardButton.Yes
