from typing import Literal
from PySide6.QtGui import QLinearGradient, QColor, QPainter
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve, Qt, QParallelAnimationGroup


class SlideContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgets = []
        self.current_index = 0
        self.animation_duration = 400
        self.easing_curve = QEasingCurve.Type.InOutQuart

    def addWidget(self, widget):
        """Add a widget to the stack and hide it if it's not the first one."""
        widget.setParent(self)
        if self.widgets:
            widget.setGeometry(self.width(), 0, self.width(), self.height())
            widget.hide()
        else:
            widget.setGeometry(0, 0, self.width(), self.height())
            widget.show()
        self.widgets.append(widget)

    def slideToIndex(self, index):
        if index == self.current_index or index < 0 or index >= len(self.widgets):
            return

        # Determine direction
        direction_right = index > self.current_index
        
        old_widget = self.widgets[self.current_index]
        new_widget = self.widgets[index]
        
        self.current_index = index
        width = self.width()

        # Position the new widget before starting
        start_pos = QPoint(width, 0) if direction_right else QPoint(-width, 0)
        end_pos_old = QPoint(-width, 0) if direction_right else QPoint(width, 0)

        new_widget.setGeometry(start_pos.x(), 0, width, self.height())
        new_widget.show()

        # Setup Animations
        self.group = QParallelAnimationGroup()

        # Outgoing animation
        self.anim_out = QPropertyAnimation(old_widget, b"pos")
        self.anim_out.setDuration(self.animation_duration)
        self.anim_out.setEasingCurve(self.easing_curve)
        self.anim_out.setEndValue(end_pos_old)

        # Incoming animation
        self.anim_in = QPropertyAnimation(new_widget, b"pos")
        self.anim_in.setDuration(self.animation_duration)
        self.anim_in.setEasingCurve(self.easing_curve)
        self.anim_in.setEndValue(QPoint(0, 0))

        self.group.addAnimation(self.anim_out)
        self.group.addAnimation(self.anim_in)
        
        # Hide old widget after animation finishes to save resources
        self.group.finished.connect(old_widget.hide)
        self.group.start()

    def resizeEvent(self, event):
        """Ensure widgets resize to match the container."""
        for i, widget in enumerate(self.widgets):
            if i == self.current_index:
                widget.setGeometry(0, 0, self.width(), self.height())
            else:
                widget.setGeometry(self.width(), 0, self.width(), self.height())
        super().resizeEvent(event)


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
