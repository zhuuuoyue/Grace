# -*- coding: utf-8 -*-

from uuid import UUID
from typing import Optional, Union

from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtGui import QCloseEvent

from ui import get_ui_cache


class DialogBase(QDialog):

    def __init__(self, dialog_id: Optional[UUID] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__dialog_id: Union[UUID, None] = None
        self.dialog_id = dialog_id

        dialog_geometry_cache = get_ui_cache().get_dialog_geometry(self.dialog_id)
        if dialog_geometry_cache is not None:
            self.resize(dialog_geometry_cache[1])
            self.move(dialog_geometry_cache[0])

    @property
    def dialog_id(self) -> Union[UUID, None]:
        return self.__dialog_id

    @dialog_id.setter
    def dialog_id(self, value: Union[UUID, None]):
        if isinstance(value, UUID):
            self.__dialog_id = value

    def closeEvent(self, event: QCloseEvent) -> None:
        get_ui_cache().update_dialog_geometry(self.dialog_id, self.pos(), self.size())
        super().closeEvent(event)
