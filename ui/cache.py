# -*- coding: utf-8 -*-

import os
import json
from typing import Optional, Union, Dict

from PySide6.QtCore import QPoint, QSize, QRect, QObject
from PySide6.QtWidgets import QDialog, QMainWindow


class DialogGeometry(object):

    def __init__(self, position: QPoint, size: QSize):
        self.position: QPoint = position
        self.size: QSize = size


_KEY_LEFT = 'left'
_KEY_TOP = 'top'
_KEY_WIDTH = 'width'
_KEY_HEIGHT = 'height'


def validate_dialog_geometry_data(data: Dict[str, int]) -> bool:
    if not isinstance(data, dict):
        return False
    keys = [_KEY_LEFT, _KEY_TOP, _KEY_WIDTH, _KEY_HEIGHT]
    for key in keys:
        if key not in data:
            return False
        if not isinstance(data[key], int):
            return False
    return True


def dict_to_dialog_geometry(data: Dict[str, int]) -> Union[DialogGeometry, None]:
    if not validate_dialog_geometry_data(data):
        return None
    return DialogGeometry(
        position=QPoint(data[_KEY_LEFT], data[_KEY_TOP]),
        size=QSize(data[_KEY_WIDTH], data[_KEY_HEIGHT])
    )


def dialog_geometry_to_dict(dialog_geometry: DialogGeometry) -> Dict[str, int]:
    return {
        _KEY_LEFT: dialog_geometry.position.x(),
        _KEY_TOP: dialog_geometry.position.y(),
        _KEY_WIDTH: dialog_geometry.size.width(),
        _KEY_HEIGHT: dialog_geometry.size.height()
    }


class DialogGeometryValidator(QObject):

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__rect: Union[QRect, None] = None
        self.update()

    def validate(self, dialog_geometry: DialogGeometry) -> bool:
        return True

    def update(self):
        pass


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
                    data = dict_to_dialog_geometry(value)
                    if data is not None:
                        self.__dialog_geometry_cache[key] = data

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
                dialog_geometry_records[dialog_geometry_key] = dialog_geometry_to_dict(dialog_geometry_value)
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
