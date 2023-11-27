# -*- coding: utf-8 -*-

from typing import Union, Optional

from shapely import Point
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout

from ui.utils import add_layout_children

from .point_input import PointInput
from .line_segment import LineSegment


class LineSegmentInput(QWidget):

    line_segment_changed = Signal(type(Union[LineSegment, None]))

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__start_point_input = PointInput()
        self.__separator = QLabel('-')
        self.__separator.setFixedWidth(8)
        self.__end_point_input = PointInput()
        self.__layout = QHBoxLayout()
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        add_layout_children(self.__layout, [self.__start_point_input, self.__separator, self.__end_point_input])
        self.setLayout(self.__layout)

        self.__start_point_input.point_changed.connect(self.__on_endpoint_changed)
        self.__end_point_input.point_changed.connect(self.__on_endpoint_changed)

    @Slot(type(Union[Point, None]))
    def __on_endpoint_changed(self, endpoint: Union[Point, None]):
        start_point = self.__start_point_input.get_point()
        end_point = self.__end_point_input.get_point()
        if start_point is None or end_point is None:
            self.line_segment_changed.emit(None)
        else:
            self.line_segment_changed.emit(LineSegment(start_point, end_point))
