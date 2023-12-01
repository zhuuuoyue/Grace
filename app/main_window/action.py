# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Signal, Slot, QObject
from PySide6.QtGui import QAction


class Action(QAction):

    clicked: Signal = Signal(str)

    def __init__(self, command_id: str, text: str, parent: Optional[QObject] = None):
        super().__init__(text=text, parent=parent)
        self.__command_id = command_id
        self.triggered.connect(self.__on_triggered)

    @Slot()
    def __on_triggered(self):
        self.clicked.emit(self.__command_id)
