# -*- coding: utf-8 -*-

__all__ = ['UICache']

import os
import json
from typing import Dict

from PySide6.QtWidgets import QDialog, QMainWindow

from .dialog_geometry import DialogGeometry
from .dialog_geometry_validator import DialogGeometryValidator
from .utils import dict_to_dialog_geometry, dialog_geometry_to_dict


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
