# -*- coding: utf-8 -*-

from typing import Optional, Dict, Union, Any

from PySide6.QtCore import QObject, Signal, Property

from tasks.create import EditTemplateTasks, TemplateData


class EditTemplatesModel(QObject):

    data_changed = Signal(type(Dict[str, str]))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__data: Dict[str, str] = dict()

    def get_data(self) -> Dict[str, str]:
        return self.__data

    def set_data(self, value: Dict[str, str]):
        if self.__data != value:
            self.__data = value
            self.data_changed.emit(self.__data)

    data = Property(type(Dict[str, str]), fget=get_data, fset=set_data, notify=data_changed)

    def get_content(self, name: str) -> Union[str, None]:
        return None if name not in self.data else self.data[name]

    def initialize(self):
        self.update()

    def update(self):
        templates = EditTemplateTasks.get_templates()
        sorted_templates = sorted(templates, key=lambda item: item.name)
        data: Dict[str, str] = dict()
        for template in sorted_templates:
            data[template.name] = template.content
        self.data = data
