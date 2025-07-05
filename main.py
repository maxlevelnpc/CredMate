import logging
import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from app.modules.misc_utils import load_qss
from app.windows.main_window.wd_main import MainWindowLogic
from app.windows.main_window.wd_ui import MainWindowUI

from app.resources import icons  # noqa

basedir = os.path.dirname(__file__)
logging.basicConfig(
    filename=os.path.join(basedir, "log", "err.log"),
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - Line %(lineno)d - %(message)s'
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowUI(self)
        self.ui.setupUi()

        self.logic = MainWindowLogic(self, self.ui)
        self.logic.setupLogic()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    stylesheet = load_qss(
        ":/app/resources/styles/base.qss",
        ":/app/resources/styles/custom.qss"
    )
    app.setStyleSheet(stylesheet)

    sys.exit(app.exec())
