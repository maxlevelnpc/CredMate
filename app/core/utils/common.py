import logging
from PySide6.QtCore import QFile, QTextStream

log = logging.getLogger(__name__)


def load_style(*paths: str) -> str:
    """
    :returns: combined styles.
    """
    style = ""

    for path in paths:
        file = QFile(path)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style += stream.readAll() + f"\n\n"
            file.close()
        else:
            log.critical(f"{file.errorString()} -> `{path}`")

    return style


def setup_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        f"[%(levelname)s] %(asctime)s | %(name)s | Ln. %(lineno)d %(funcName)s -> %(message)s",
        "%Y-%m-%d %I:%M:%S %p"
    )

    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    root.addHandler(file_handler)
    root.addHandler(console_handler)