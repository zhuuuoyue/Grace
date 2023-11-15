# -*- coding: utf-8 -*-

from typing import Optional, Dict

from PySide6.QtCore import QObject, Signal, Property


class EditTemplateModel(QObject):

    data_changed = Signal(type(Dict[str, str]))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__data: Dict[str, str] = dict()

    def get_data(self) -> Dict[str, str]:
        return self.__data

    def set_data(self, value: Dict[str, str]):
        if self.__data != value:
            self.__data = value
            self.data_changed.emit(self.__data)

    data = Property(type(Dict[str, str]), fget=get_data, fset=set_data, notify=data_changed)

    def initialize(self):
        fake = {
            "cpp": "hello c plus plus",
            "python": "hello python"
        }
        self.data = fake
