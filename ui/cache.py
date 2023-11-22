# -*- coding: utf-8 -*-

import os
import json
from typing import Optional, Union, Dict, List

from PySide6.QtCore import QPoint, QSize, QRect, QObject, Slot
from PySide6.QtWidgets import QDialog, QMainWindow
from PySide6.QtGui import QGuiApplication, QScreen


class DialogGeometry(object):

    _KEY_LEFT = 'left'
    _KEY_TOP = 'top'
    _KEY_WIDTH = 'width'
    _KEY_HEIGHT = 'height'

    def __init__(self, position: QPoint, size: QSize):
        self.position: QPoint = position
        self.size: QSize = size

    @staticmethod
    def from_dict(data: Dict[str, int]):
        return DialogGeometry(
            position=QPoint(data[DialogGeometry._KEY_LEFT], data[DialogGeometry._KEY_TOP]),
            size=QSize(data[DialogGeometry._KEY_WIDTH], data[DialogGeometry._KEY_HEIGHT])
        )

    def to_dict(self) -> Dict[str, int]:
        return {
            DialogGeometry._KEY_LEFT: self.position.x(),
            DialogGeometry._KEY_TOP: self.position.y(),
            DialogGeometry._KEY_WIDTH: self.size.width(),
            DialogGeometry._KEY_HEIGHT: self.size.height()
        }


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


class UICache(object):

    _CACHE_DIRECTORY = 'cache'
    _DIALOG_GEOMETRY_CACHE_FILENAME = 'dialog_geometry.json'

    _DIALOG_GEOMETRY_KEY = 'dialog_geometry'

    def __init__(self, workspace_path: str):
        self.__cache_directory: str = os.path.join(workspace_path, UICache._CACHE_DIRECTORY)
        self.__dialog_geometry_cache: Dict[str, DialogGeometry] = dict()
        self.__dialog_geometry_validator = DialogGeometryValidator()

    def update_dialog_geometry_cache(self, dialog: [QDialog, QMainWindow]):
        dialog_object_name = dialog.objectName()
        if len(dialog_object_name) != 0:
            self.__dialog_geometry_cache[dialog_object_name] = DialogGeometry(
                position=dialog.pos(),
                size=dialog.size()
            )

    def update_dialog_geometry(self, dialog: [QDialog, QMainWindow]):
        dialog_object_name = dialog.objectName()
        if len(dialog_object_name) != 0 and dialog_object_name in self.__dialog_geometry_cache:
            dialog_geometry = self.__dialog_geometry_cache[dialog_object_name]
            if self.__dialog_geometry_validator.validate(dialog_geometry):
                dialog.resize(dialog_geometry.size)
                dialog.move(dialog_geometry.position)

    def load(self):
        dialog_geometry_cache_file_path = os.path.join(self.__cache_directory, UICache._DIALOG_GEOMETRY_CACHE_FILENAME)
        if os.path.isfile(dialog_geometry_cache_file_path):
            with open(dialog_geometry_cache_file_path, 'r') as fp:
                raw_data = json.load(fp)

                dialog_geometry_cache = raw_data[UICache._DIALOG_GEOMETRY_KEY]
                for key in dialog_geometry_cache:
                    value = dialog_geometry_cache[key]
                    self.__dialog_geometry_cache[key] = DialogGeometry.from_dict(value)

    def save(self):
        if not os.path.isdir(self.__cache_directory):
            os.mkdir(self.__cache_directory)
        dialog_geometry_cache_file_path = os.path.join(self.__cache_directory, UICache._DIALOG_GEOMETRY_CACHE_FILENAME)
        with open(dialog_geometry_cache_file_path, 'w') as fp:
            to_write = dict()

            # dialog geometry
            dialog_geometry_records = dict()
            for dialog_geometry_key in self.__dialog_geometry_cache:
                dialog_geometry_value = self.__dialog_geometry_cache[dialog_geometry_key]
                dialog_geometry_records[dialog_geometry_key] = dialog_geometry_value.to_dict()
            to_write[UICache._DIALOG_GEOMETRY_KEY] = dialog_geometry_records

            text = json.dumps(to_write, indent=4)
            fp.write(text)


_ui_cache: Union[UICache, None] = None


def get_ui_cache() -> UICache:
    return _ui_cache


def initialize_ui_cache(workspace_directory: str):
    global _ui_cache
    _ui_cache = UICache(workspace_directory)
    _ui_cache.load()


def update_dialog_geometry_cache(dialog: [QDialog, QMainWindow], flush: Optional[bool] = False):
    get_ui_cache().update_dialog_geometry_cache(dialog)
    if flush:
        get_ui_cache().save()


def update_dialog_geometry(dialog: [QDialog, QMainWindow]):
    get_ui_cache().update_dialog_geometry(dialog)
