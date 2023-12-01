# -*- coding: utf-8 -*-

__all__ = [
    'initialize_ui_cache',
    'update_dialog_geometry',
    'update_dialog_geometry_cache',
    'flush_dialog_geometry_cache'
]

from typing import Union, Optional

from PySide6.QtWidgets import QDialog, QMainWindow

from .ui_cache import UICache


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


def flush_dialog_geometry_cache():
    get_ui_cache().save()


def update_dialog_geometry(dialog: [QDialog, QMainWindow]):
    get_ui_cache().update_dialog_geometry(dialog)
