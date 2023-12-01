# -*- coding: utf-8 -*-

__all__ = ['EnvironmentButton']

from typing import Optional

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QPushButton, QWidget

from extensions.glodon.environment import Environment


class EnvironmentButton(QPushButton):

    request_switching_environment = Signal(Environment)

    def __init__(self, environment: Environment, name: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setText(name)
        self.__environment = environment
        self.clicked.connect(self.__on_clicked)

    @Slot()
    def __on_clicked(self):
        self.request_switching_environment.emit(self.__environment)
