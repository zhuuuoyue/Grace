# -*- coding: utf-8 -*-

__all__ = ['WidgetModelBase']

from abc import abstractmethod
from typing import Optional

from PySide6.QtCore import QObject


class WidgetModelBase(QObject):

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def update(self):
        pass
