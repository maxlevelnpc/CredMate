import sys

from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QApplication, QMainWindow

from main_window.wd_main import MainWindowLogic
from main_window.wd_ui import MainWindowUI


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowUI(self)
        self.ui.setupUi()

        self.logic = MainWindowLogic(self.ui)
        self.logic.setupLogic()

        self.custom_width = 800  # Set your desired width here (in pixels)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
