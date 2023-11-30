# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLineEdit
from PySide6.QtGui import QKeyEvent, QFocusEvent


class KeywordInput(QLineEdit):

    key_up_pressed = Signal()
    key_down_pressed = Signal()
    key_enter_pressed = Signal()
    key_escape_pressed = Signal()
    focus_lost = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Escape:
            self.key_escape_pressed.emit()
        elif event.key() == Qt.Key.Key_Up:
            self.key_up_pressed.emit()
        elif event.key() == Qt.Key.Key_Down:
            self.key_down_pressed.emit()
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.key_enter_pressed.emit()

    def focusOutEvent(self, event: QFocusEvent):
        super().focusOutEvent(event)
        self.focus_lost.emit()
