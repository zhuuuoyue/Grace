# -*- coding: utf-8 -*-

from typing import Optional, Union

import numpy as np
from PySide6.QtCore import Signal, Slot, Property, QObject

from ui import WidgetViewModelBase

from .algorithm import SpatialRelationship
from .infer_spatial_relationship_model import InferSpatialRelationshipModel


class InferSpatialRelationshipViewModel(WidgetViewModelBase):

    angle_text_changed = Signal(type(str))
    conclusion_text_changed = Signal(type(str))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__model = InferSpatialRelationshipModel(self)
        self.__angle_text: str = str()
        self.__conclusion_text: str = str()

    @property
    def model(self) -> InferSpatialRelationshipModel:
        return self.__model

    def get_angle_text(self) -> str:
        return self.__angle_text

    def set_angle_text(self, value: str):
        if self.angle_text != value:
            self.__angle_text = value
            self.angle_text_changed.emit(self.angle_text)

    angle_text = Property(type(str), fget=get_angle_text, fset=set_angle_text, notify=angle_text_changed)

    def get_conclusion_text(self) -> str:
        return self.__conclusion_text

    def set_conclusion_text(self, value: str):
        if self.conclusion_text != value:
            self.__conclusion_text = value
            self.conclusion_text_changed.emit(self.conclusion_text)

    conclusion_text = Property(type(str), fget=get_conclusion_text, fset=set_conclusion_text,
                               notify=conclusion_text_changed)

    def initialize(self):
        self.model.angle_changed.connect(self.__on_model_angle_changed)
        self.model.conclusion_changed.connect(self.__on_model_conclusion_changed)
        self.model.initialize()

    def update(self):
        self.model.update()

    @Slot(type(Union[float, None]))
    def __on_model_angle_changed(self, angle: Union[float, None]):
        self.angle_text = str() if angle is None else f'{angle} degree(s), {np.radians(angle)} radian(s)'

    @Slot(type(SpatialRelationship))
    def __on_model_conclusion_changed(self, conclusion: SpatialRelationship):
        self.conclusion_text = {
            SpatialRelationship.UNKNOWN: '',
            SpatialRelationship.PARALLEL: 'Parallel',
            SpatialRelationship.PERPENDICULAR: 'Perpendicular',
        }[conclusion]
