import logging
import os
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from app.services.credential_service import CredentialService
from app.utils.misc_utils import load_qss
from app.views.main_view import MainView
from app.presenters.main_presenter import MainPresenter
from app.models.credential_model import CredentialModel

from assets import icons

basedir = os.path.dirname(__file__)
logging.basicConfig(
    filename=os.path.join(basedir, "err.log"),
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - Line %(lineno)d - %(message)s'
)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    cred_service = CredentialService()
    cred_model = CredentialModel(cred_service)
    view = MainView()
    presenter = MainPresenter(cred_model, view)
    view.show()

    stylesheet = load_qss(
        "assets/styles/base.qss",
        "assets/styles/custom.qss"
    )
    app.setStyleSheet(stylesheet)

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        pass
