# -*- coding: utf-8 -*-

__all__ = ['DialogGeometryValidator']

from typing import Optional, List

from PySide6.QtCore import QObject, QRect, Slot
from PySide6.QtGui import QScreen, QGuiApplication

from .dialog_geometry import DialogGeometry


class DialogGeometryValidator(QObject):

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__screens: List[QScreen] = list()
        self.__rectangles: List[QRect] = list()
        self.update()

    def validate(self, dialog_geometry: DialogGeometry) -> bool:
        for screen_rect in self.__rectangles:
            dialog_rect = QRect(dialog_geometry.position, dialog_geometry.size)
            intersected = screen_rect.intersected(dialog_rect)
            if intersected.isEmpty():
                continue
            if dialog_rect.top() >= screen_rect.top():
                return True
        return False

    def update(self):
        for screen in self.__screens:
            screen.availableGeometryChanged.disconnect(self.__on_available_geometry_changed)
        self.__screens = QGuiApplication.screens()
        for screen in self.__screens:
            self.__rectangles.append(screen.availableGeometry())
            screen.availableGeometryChanged.connect(self.__on_available_geometry_changed)

    @Slot(QRect)
    def __on_available_geometry_changed(self, geometry: QRect):
        self.update()
