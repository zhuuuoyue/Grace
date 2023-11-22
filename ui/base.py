# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QMainWindow, QWidget, QApplication
from PySide6.QtGui import QCloseEvent

from .cache import update_dialog_geometry, update_dialog_geometry_cache


class DialogBase(QDialog):

    def __init__(self, object_name: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName(object_name)
        update_dialog_geometry(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        update_dialog_geometry_cache(self)
        super().closeEvent(event)


class MainWindowBase(QMainWindow):

    def __init__(self, object_name: Optional[str] = None, parent: Optional[QWidget] = None,
                 flags: Qt.WindowType = Qt.WindowType.Window):
        super().__init__(parent, flags)
        if isinstance(object_name, str):
            self.setObjectName(object_name)
        update_dialog_geometry(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        update_dialog_geometry_cache(self, True)
        super().closeEvent(event)


class ApplicationBase(QApplication):

    def __init__(self, args: Sequence[str]):
        super().__init__(args)
