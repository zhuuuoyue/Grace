# -*- coding: utf-8 -*-

import re
from typing import Optional, Set

from PySide6.QtCore import QObject, Signal, Slot, Property

from ui.create.EditTemplate.TemplateData import TemplateData


class TemplateEditorModel(QObject):

    parameter_pattern = re.compile('\$\{(\w[\w\d]*)\}')

    name_changed = Signal(str)
    content_changed = Signal(str)
    parameters_changed = Signal(type(Set[str]))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__name: str = str()
        self.__content: str = str()
        self.__parameters: Set[str] = set()

        self.content_changed.connect(self.on_content_changed)

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

    def set_name(self, value: str):
        if value != self.name:
            self.__name = value
            self.name_changed.emit(self.name)

    def get_content(self) -> str:
        return self.__content

    def set_content(self, value: str):
        if value != self.content:
            self.__content = value
            self.content_changed.emit(self.content)

    def get_parameters(self) -> Set[str]:
        return self.__parameters

    def set_parameters(self, value: Set[str]):
        if value != self.parameters:
            self.__parameters = value
            self.parameters_changed.emit(self.parameters)

    name = Property(str, fget=get_name, fset=set_name, notify=name_changed)
    content = Property(str, fget=get_content, fset=set_content, notify=content_changed)
    parameters = Property(type(Set[str]), fget=get_parameters, fset=set_parameters, notify=parameters_changed)

    @Slot(str)
    def on_content_changed(self, content: str):
        result = re.findall(self.parameter_pattern, content)
        self.set_parameters(set(result))
