# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtGui import QCloseEvent

from ui.basic.UICache import update_dialog_geometry, update_dialog_geometry_cache


class DialogBase(QDialog):

    def __init__(self, object_name: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName(object_name)
        update_dialog_geometry(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        update_dialog_geometry_cache(self)
        super().closeEvent(event)
