from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QPoint, QEvent, QSize
from PySide6.QtGui import QIcon

class BackButton(QPushButton):
    def __init__(self, parent, icon_path, size=56):
        super().__init__(parent)
        
        self._offset = QPoint(20, 20)
        self._button_size = size

        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(size // 2, size // 2))
        
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if parent:
            parent.installEventFilter(self)
            self.updatePosition()

    def setOffset(self, offset_x=None, offset_y=None):
        if offset_x is not None and offset_y is not None:
            self._offset = QPoint(offset_x, offset_y)
        self.updatePosition()

    def updatePosition(self):
        if not self.parentWidget():
            return

        ox, oy = self._offset.x(), self._offset.y()
        self.move(ox, oy)
        self.raise_()

    def eventFilter(self, obj, event):
        if obj == self.parentWidget() and event.type() == QEvent.Type.Resize:
            self.updatePosition()
        return super().eventFilter(obj, event)

    def setFixedSize(self, w, h):
        super().setFixedSize(w, h)
        self.updatePosition()


