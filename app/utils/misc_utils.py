import logging

from PySide6.QtCore import QFile, QTextStream


def load_qss(*resource_paths: str) -> str:
    """
    Load and combine multiple QSS files from Qt resource paths.
    """
    qss = ""
    try:
        for path in resource_paths:
            file = QFile(path)
            if file.exists() and file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                qss += stream.readAll() + "\n"
                file.close()
    except Exception as e:
        logging.error(f"Failed to load QSS: {e}")

    return qss
