# -*- coding: utf-8 -*-

from typing import Optional, Union

import numpy as np
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QCloseEvent

from ui import DialogBase
from ui.cache import get_ui_cache

from .line_segment import LineSegment
from .infer_spatial_relationship_view import InferSpatialRelationshipView
from .infer_spatial_relationship_view_model import InferSpatialRelationshipViewModel


class InferSpatialRelationshipDialog(DialogBase):

    __instance__ = None

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(object_name='6a69811c-e16c-43b9-b14d-7a10df891fd9', parent=parent)
        self.__ui = InferSpatialRelationshipView(self)
        self.__vm = InferSpatialRelationshipViewModel(self)

    @staticmethod
    def get_dialog():
        if InferSpatialRelationshipDialog.__instance__ is None:
            dialog = InferSpatialRelationshipDialog()
            dialog.setWindowModality(Qt.WindowModality.NonModal)
            dialog.initialize()
            InferSpatialRelationshipDialog.__instance__ = dialog
        return InferSpatialRelationshipDialog.__instance__

    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        InferSpatialRelationshipDialog.__instance__ = None
        get_ui_cache().save()

    def initialize(self):
        # signals from view
        self.__ui.first_line_segment_input.line_segment_changed.connect(self.__on_ui_first_line_segment_changed)
        self.__ui.second_line_segment_input.line_segment_changed.connect(self.__on_ui_second_line_segment_changed)
        self.__ui.degree_input.value_changed.connect(self.__on_ui_tolerance_degree_value_changed)
        self.__ui.radian_input.value_changed.connect(self.__on_ui_tolerance_radian_value_changed)

        # signals from view model
        self.__vm.angle_text_changed.connect(self.__ui.angle.setText)
        self.__vm.conclusion_text_changed.connect(self.__ui.conclusion.setText)

        # signals from model
        self.__vm.model.tolerance_changed.connect(self.__on_model_tolerance_degree_value_changed)
        self.__vm.model.tolerance_changed.connect(self.__on_model_tolerance_radian_value_changed)

        # initialize
        self.__vm.initialize()

    @Slot(type(Union[LineSegment, None]))
    def __on_ui_first_line_segment_changed(self, line_segment: Union[LineSegment, None]):
        self.__vm.model.first_line_segment = line_segment
        if line_segment is None:
            self.__ui.visualizer.remove_first_line_segment()
        else:
            self.__ui.visualizer.update_first_line_segment(line_segment)

    @Slot(type(Union[LineSegment, None]))
    def __on_ui_second_line_segment_changed(self, line_segment: Union[LineSegment, None]):
        self.__vm.model.second_line_segment = line_segment
        if line_segment is None:
            self.__ui.visualizer.remove_second_line_segment()
        else:
            self.__ui.visualizer.update_second_line_segment(line_segment)

    @Slot(type(Union[float, None]))
    def __on_ui_tolerance_degree_value_changed(self, value: Union[float, None]):
        self.__vm.model.tolerance = value

    @Slot(type(Union[float, None]))
    def __on_ui_tolerance_radian_value_changed(self, value: Union[float, None]):
        self.__vm.model.tolerance = None if value is None else np.degrees(value)

    @Slot(type(Union[float, None]))
    def __on_model_tolerance_degree_value_changed(self, value: Union[float, None]):
        self.__ui.degree_input.set_value(value)

    @Slot(type(Union[float, None]))
    def __on_model_tolerance_radian_value_changed(self, value: Union[float, None]):
        if value is None:
            self.__ui.radian_input.set_value(None)
        else:
            self.__ui.radian_input.set_value(np.radians(value))
