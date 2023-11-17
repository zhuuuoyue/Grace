# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import QObject, Signal, Slot, Property

from tasks.create import TemplateData


class TemplateEditorModel(QObject):

    name_changed = Signal(str)
    content_changed = Signal(str)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__name: str = str()
        self.__content: str = str()

    def load_data(self, data: TemplateData):
        self.name = data.name
        self.content = data.content

    def get_data(self) -> TemplateData:
        data = TemplateData()
        data.name = self.name
        data.content = self.content
        return data

    def get_name(self) -> str:
        return self.__name

    @Slot(str)
    def set_name(self, value: str):
        if value != self.name:
            self.__name = value
            self.name_changed.emit(self.name)

    name = Property(str, fget=get_name, fset=set_name, notify=name_changed)

    def get_content(self) -> str:
        return self.__content

    @Slot(str)
    def set_content(self, value: str):
        if value != self.content:
            self.__content = value
            self.content_changed.emit(self.content)

    content = Property(str, fget=get_content, fset=set_content, notify=content_changed)
