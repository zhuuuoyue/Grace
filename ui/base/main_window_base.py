# -*- coding: utf-8 -*-

__all__ = ['MainWindowBase']

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtGui import QCloseEvent

from ui.cache import update_dialog_geometry, update_dialog_geometry_cache
from ui.components import Icon


class MainWindowBase(QMainWindow):

    def __init__(self,
                 object_name: Optional[str] = None,
                 parent: Optional[QWidget] = None,
                 flags: Qt.WindowType = Qt.WindowType.Window,
                 window_icon: Optional[str] = None,
                 window_title: Optional[str] = None):
        super().__init__(parent, flags)
        if isinstance(object_name, str):
            self.setObjectName(object_name)
        update_dialog_geometry(self)
        self.setWindowIcon(Icon(window_icon))
        self.setWindowTitle(str() if window_title is None else window_title)

    def closeEvent(self, event: QCloseEvent) -> None:
        update_dialog_geometry_cache(self, True)
        super().closeEvent(event)
