from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve, QParallelAnimationGroup


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
        """Index based on widget added order"""
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
        
        self.group.finished.connect(old_widget.hide)
        self.group.start()

    def resizeEvent(self, event):
        """make sure widgets resize to match the container."""
        for i, widget in enumerate(self.widgets):
            if i == self.current_index:
                widget.setGeometry(0, 0, self.width(), self.height())
            else:
                widget.setGeometry(self.width(), 0, self.width(), self.height())
        super().resizeEvent(event)