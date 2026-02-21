import logging
import sys

from PySide6.QtWidgets import QApplication

from app.models import CredentialModel
from app.presenters import MainPresenter
from app.views import MainView
from app.core.services import CredentialService
from app.core.utils import load_style, setup_logging

from app.assets import res_rc

setup_logging()

log = logging.getLogger(__name__)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    service = CredentialService()
    model = CredentialModel(service)
    view = MainView()
    presenter = MainPresenter(model, view)
    view.show()

    stylesheet = load_style(
        ":/app/assets/styles/base.css",
        ":/app/assets/styles/custom.css"
    )
    app.setStyleSheet(stylesheet)

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        pass
