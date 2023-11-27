# -*- coding: utf-8 -*-

from typing import Union, Optional

from shapely import Point
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

from ui.utils import add_layout_children

from .double_input import DoubleInput


def create_symbol_label(text: str) -> QLabel:
    label = QLabel()
    label.setFixedWidth(8)
    label.setText(text)
    return label


class PointInput(QWidget):

    point_changed = Signal(type(Union[Point, None]))

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        css = '''font-family: 'consolas';
        font-size: 13px;
        border: none;
        '''
        self.__left_parenthesis = create_symbol_label('(')
        self.__x_input = DoubleInput()
        self.__x_input.setStyleSheet(css)
        self.__comma = create_symbol_label(',')
        self.__y_input = DoubleInput()
        self.__y_input.setStyleSheet(css)
        self.__right_parenthesis = create_symbol_label(')')
        self.__layout = QHBoxLayout()
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        add_layout_children(
            self.__layout,
            [self.__left_parenthesis, self.__x_input, self.__comma, self.__y_input, self.__right_parenthesis]
        )
        self.setLayout(self.__layout)

        self.__x_input.value_changed.connect(self.__on_dimension_value_changed)
        self.__y_input.value_changed.connect(self.__on_dimension_value_changed)

    def get_point(self) -> Union[Point, None]:
        x = self.__x_input.get_value()
        y = self.__y_input.get_value()
        if x is None or y is None:
            return None
        else:
            return Point(x, y)

    @Slot(type(Union[float, None]))
    def __on_dimension_value_changed(self, value: Union[float, None]):
        self.point_changed.emit(self.get_point())
