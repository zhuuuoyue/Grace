# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QListView
from PySide6.QtGui import QFocusEvent


class CandidateList(QListView):

    focus_lost = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    def focusOutEvent(self, event: QFocusEvent):
        super().focusOutEvent(event)
        self.focus_lost.emit()
