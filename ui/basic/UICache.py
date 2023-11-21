# -*- coding: utf-8 -*-

import os
import json
from typing import Union, Dict

from PySide6.QtCore import QPoint, QSize
from PySide6.QtWidgets import QDialog, QMainWindow


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


class UICache(object):

    _CACHE_DIRECTORY = 'cache'
    _DIALOG_GEOMETRY_CACHE_FILENAME = 'dialog_geometry.json'

    _DIALOG_GEOMETRY_KEY = 'dialog_geometry'

    def __init__(self, workspace_path: str):
        self.__cache_directory: str = os.path.join(workspace_path, UICache._CACHE_DIRECTORY)
        self.__dialog_geometry_cache: Dict[str, DialogGeometry] = dict()

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
            record = self.__dialog_geometry_cache[dialog_object_name]
            dialog.resize(record.size)
            dialog.move(record.position)

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


def flush_ui_cache():
    get_ui_cache().save()


def update_dialog_geometry_cache(dialog: [QDialog, QMainWindow]):
    get_ui_cache().update_dialog_geometry_cache(dialog)


def update_dialog_geometry(dialog: [QDialog, QMainWindow]):
    get_ui_cache().update_dialog_geometry(dialog)
