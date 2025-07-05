from typing import Literal
from PySide6.QtGui import QLinearGradient, QColor, QPainter
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve, Qt


class Container(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#1d2026"))
        gradient.setColorAt(0.5, QColor("#1a2031"))
        gradient.setColorAt(1, QColor("#1d2026"))
        painter.fillRect(self.rect(), gradient)

    def moveContainer(
            self,
            move_mode: Literal["show_left", "show_right", "hide_left", "hide_right"],
            duration=200
    ):
        """
        Animates the widget movement based on the move_mode.
        """
        valid_modes = {"show_left", "show_right", "hide_left", "hide_right"}
        if move_mode not in valid_modes:
            return

        if hasattr(self, '_animation') and self._animation.state() == QPropertyAnimation.State.Running:  # noqa
            return

        # Create new animation
        self._animation = QPropertyAnimation(self, b"pos")  # noqa
        self._animation.setDuration(duration)

        # Current position
        current_pos = self.pos()
        parent_width = self.parent().width() if self.parent() and self.parent().width() > 0 else 800  # Fallback

        # Define start and target positions
        if move_mode == "show_left":
            start_pos = QPoint(-self.width(), current_pos.y())
            target_pos = QPoint(0, current_pos.y())
        elif move_mode == "show_right":
            start_pos = QPoint(parent_width, current_pos.y())
            target_pos = QPoint(0, current_pos.y())
        elif move_mode == "hide_left":
            start_pos = QPoint(0, current_pos.y())
            target_pos = QPoint(-self.width(), current_pos.y())
        else:  # hide_right
            start_pos = QPoint(0, current_pos.y())
            target_pos = QPoint(parent_width, current_pos.y())

        self.move(start_pos)

        if move_mode.startswith("show"):
            self._animation.setEasingCurve(QEasingCurve.Type.OutQuint)
        else:
            self._animation.setEasingCurve(QEasingCurve.Type.InQuint)

        self._animation.setStartValue(start_pos)
        self._animation.setEndValue(target_pos)
        self._animation.start()
