# -*- coding: utf-8 -*-

from typing import Union, Optional

import numpy as np
from PySide6.QtCore import Signal, Slot, Property, QObject

from ui import WidgetModelBase
from shared import math as m

from .line_segment import LineSegment
from .algorithm import SpatialRelationship, is_close, calculate_angle, infer_spatial_relationship


class InferSpatialRelationshipModel(WidgetModelBase):

    first_line_segment_changed = Signal(type(Union[LineSegment, None]))
    second_line_segment_changed = Signal(type(Union[LineSegment, None]))
    angle_changed = Signal(type(Union[float, None]))
    tolerance_changed = Signal(type(Union[float, None]))
    conclusion_changed = Signal(type(SpatialRelationship))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__first_line_segment: Union[LineSegment, None] = None
        self.__second_line_segment: Union[LineSegment, None] = None
        self.__angle: Union[float, None] = None
        self.__tolerance: Union[float, None] = None
        self.__conclusion: SpatialRelationship = SpatialRelationship.UNKNOWN

    def get_first_line_segment(self) -> Union[LineSegment, None]:
        return self.__first_line_segment

    def set_first_line_segment(self, value: Union[LineSegment, None]):
        if self.first_line_segment != value:
            self.__first_line_segment = value
            self.first_line_segment_changed.emit(self.first_line_segment)

    first_line_segment = Property(
        type(Union[LineSegment, None]),
        fget=get_first_line_segment,
        fset=set_first_line_segment,
        notify=first_line_segment_changed
    )

    def get_second_line_segment(self) -> Union[LineSegment, None]:
        return self.__second_line_segment

    def set_second_line_segment(self, value: Union[LineSegment, None]):
        if self.second_line_segment != value:
            self.__second_line_segment = value
            self.second_line_segment_changed.emit(self.second_line_segment)

    second_line_segment = Property(
        type(Union[LineSegment, None]),
        fget=get_second_line_segment,
        fset=set_second_line_segment,
        notify=second_line_segment_changed
    )

    def get_angle(self) -> Union[float, None]:
        return self.__angle

    def set_angle(self, value: Union[float, None]):
        if not is_close(self.angle, value):
            self.__angle = value
            self.angle_changed.emit(self.angle)

    angle = Property(type(Union[float, None]), fget=get_angle, fset=set_angle, notify=angle_changed)

    def get_tolerance(self) -> Union[float, None]:
        return self.__tolerance

    def set_tolerance(self, value: Union[float, None]):
        if not is_close(self.tolerance, value):
            self.__tolerance = value
            self.tolerance_changed.emit(self.tolerance)

    tolerance = Property(type(Union[float, None]), fget=get_tolerance, fset=set_tolerance, notify=tolerance_changed)

    def get_conclusion(self) -> SpatialRelationship:
        return self.__conclusion

    def set_conclusion(self, value: SpatialRelationship):
        if self.conclusion != value:
            self.__conclusion = value
            self.conclusion_changed.emit(self.conclusion)

    conclusion = Property(type(SpatialRelationship), fget=get_conclusion, fset=set_conclusion,
                          notify=conclusion_changed)

    def initialize(self):
        # connect
        self.first_line_segment_changed.connect(self.__on_first_line_segment_changed)
        self.second_line_segment_changed.connect(self.__on_second_line_segment_changed)
        self.angle_changed.connect(self.__on_angle_changed)
        self.tolerance_changed.connect(self.__on_tolerance_changed)
        # update
        self.update()

    def update(self):
        self.tolerance = np.degrees(m.FLOAT_TOLERANCE)

    def update_angle(self):
        if self.first_line_segment is None or self.second_line_segment is None:
            self.angle = None
        else:
            ok, angle, error = calculate_angle(self.get_first_line_segment(), self.get_second_line_segment())
            self.angle = angle if ok else None

    def update_conclusion(self):
        if self.angle is None:
            self.conclusion = SpatialRelationship.UNKNOWN
        else:
            self.conclusion = infer_spatial_relationship(self.angle, self.tolerance)

    @Slot(type(Union[LineSegment, None]))
    def __on_first_line_segment_changed(self, first_line_segment: Union[LineSegment, None]):
        self.update_angle()

    @Slot(type(Union[LineSegment, None]))
    def __on_second_line_segment_changed(self, second_line_segment: Union[LineSegment, None]):
        self.update_angle()

    @Slot(type(Union[float, None]))
    def __on_angle_changed(self, angle: Union[float, None]):
        self.update_conclusion()

    @Slot(type(Union[float, None]))
    def __on_tolerance_changed(self, tolerance: Union[float, None]):
        self.update_conclusion()
