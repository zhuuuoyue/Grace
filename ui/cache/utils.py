# -*- coding: utf-8 -*-

__all__ = ['validate_dialog_geometry_data', 'dict_to_dialog_geometry', 'dialog_geometry_to_dict']

from typing import Union, Dict

from PySide6.QtCore import QSize, QPoint

from .dialog_geometry import DialogGeometry


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
