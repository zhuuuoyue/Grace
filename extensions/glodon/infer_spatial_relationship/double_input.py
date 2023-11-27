# -*- coding: utf-8 -*-

from typing import Union, Optional

from PySide6.QtCore import Signal, Slot, Property
from PySide6.QtWidgets import QWidget, QLineEdit

from shared import math as m

from .algorithm import is_close


class DoubleInput(QLineEdit):

    value_changed = Signal(type(Union[float, None]))

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.editingFinished.connect(self.__on_editing_finished)
        self.__value: Union[float, None] = None

    def get_value(self) -> Union[float, None]:
        return self.__value

    def set_value(self, value: Union[float, None]):
        if self.value != value:
            self.__value = value
            self.update_view()
            self.value_changed.emit(self.value)

    value = Property(type(Union[float, None]), fget=get_value, fset=set_value, notify=value_changed)

    def update_view(self):
        current_value = self.get_value_from_input(self.text())
        if not is_close(current_value, self.value, m.FLOAT_TOLERANCE):
            if self.value is None:
                self.setText('')
            else:
                self.setText(f'{self.value:.7f}')

    @Slot()
    def __on_editing_finished(self):
        self.value = self.get_value_from_input(self.text())

    @staticmethod
    def get_value_from_input(text: str) -> Union[float, None]:
        try:
            value = float(text)
            return value
        except ValueError:
            return None
