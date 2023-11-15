# -*- coding: utf-8 -*-

from typing import Optional, List

from PySide6.QtCore import QObject, Signal, Slot, Property

from ui.create.EditTemplate.TemplateData import TemplateData

from .TemplateEditorModel import TemplateEditorModel


class TemplateEditorViewModel(QObject):

    name_text_changed = Signal(str)
    content_text_changed = Signal(str)
    parameters_text_changed = Signal(str)
    confirm_enabled_changed = Signal(bool)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__name_text: str = str()
        self.__content_text: str = str()
        self.__parameters_text: str = str()
        self.__confirm_enabled: bool = False

        self.model = TemplateEditorModel(self)

        self.model.name_changed.connect(self.on_model_name_changed)
        self.model.content_changed.connect(self.set_content_text)
        self.model.parameters_changed.connect(self.on_model_parameters_changed)

    def load_data(self, data: TemplateData):
        self.model.load_data(data)

    def get_data(self) -> TemplateData:
        return self.model.get_data()

    def get_name_text(self) -> str:
        return self.__name_text

    def set_name_text(self, value: str):
        if value != self.name_text:
            self.__name_text = value
            self.name_text_changed.emit(self.name_text)

    def set_name(self, value: str):
        self.model.set_name(value)

    def get_content_text(self) -> str:
        return self.__content_text

    def set_content_text(self, value: str):
        if value != self.content_text:
            self.__content_text = value
            self.content_text_changed.emit(self.content_text)

    def set_content(self, value: str):
        self.model.set_content(value)

    def get_parameters_text(self) -> str:
        return self.__parameters_text

    def set_parameters_text(self, value: str):
        if value != self.parameters_text:
            self.__parameters_text = value
            self.parameters_text_changed.emit(self.parameters_text)

    def get_confirm_enabled(self) -> bool:
        return self.__confirm_enabled

    def set_confirm_enabled(self, value: bool):
        if value != self.confirm_enabled:
            self.__confirm_enabled = value
            self.confirm_enabled_changed.emit(self.confirm_enabled)

    name_text = Property(str, fget=get_name_text, fset=set_name_text, notify=name_text_changed)
    content_text = Property(str, fget=get_content_text, fset=set_content_text, notify=content_text_changed)
    parameters_text = Property(str, fget=get_parameters_text, fset=set_parameters_text, notify=parameters_text_changed)
    confirm_enabled = Property(str, fget=get_confirm_enabled, fset=set_confirm_enabled, notify=confirm_enabled_changed)

    @Slot(str)
    def on_model_name_changed(self, name: str):
        self.name_text = name
        self.confirm_enabled = len(name) != 0

    @Slot(type(List[str]))
    def on_model_parameters_changed(self, parameters: List[str]):
        self.parameters_text = ', '.join(parameters)
