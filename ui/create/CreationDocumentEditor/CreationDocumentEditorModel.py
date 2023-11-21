# -*- coding: utf-8 -*-

from typing import Optional, List

from PySide6.QtCore import QObject, Slot, Signal, Property

from tasks.create import Encoding, TemplateData, EditDocumentTasks, EditTemplateTasks


class CreationDocumentEditorModel(QObject):

    relative_path_changed = Signal(str)
    encodings_changed = Signal(type(List[Encoding]))
    selected_encoding_changed = Signal(int)
    templates_changed = Signal(type(List[TemplateData]))
    selected_template_changed = Signal(int)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__relative_path: str = str()
        self.__encodings: List[Encoding] = list()
        self.__selected_encoding: int = 0
        self.__templates: List[TemplateData] = list()
        self.__selected_template: int = 0

    # relative_path

    def get_relative_path(self) -> str:
        return self.__relative_path

    def set_relative_path(self, value: str):
        if self.relative_path != value:
            self.__relative_path = value
            self.relative_path_changed.emit(self.relative_path)

    relative_path = Property(
        str,
        fget=get_relative_path,
        fset=set_relative_path,
        notify=relative_path_changed
    )

    # encodings

    def get_encodings(self) -> List[Encoding]:
        return self.__encodings

    def set_encodings(self, value: List[Encoding]):
        if self.encodings != value:
            self.__encodings = value
            self.encodings_changed.emit(self.encodings)

    encodings = Property(
        type(List[Encoding]),
        fget=get_encodings,
        fset=set_encodings,
        notify=encodings_changed
    )

    # selected_encoding

    def get_selected_encoding(self) -> int:
        return self.__selected_encoding

    def set_selected_encoding(self, value: int):
        if self.selected_encoding != value:
            self.__selected_encoding = value
            self.selected_encoding_changed.emit(self.selected_encoding)

    selected_encoding = Property(
        int,
        fget=get_selected_encoding,
        fset=set_selected_encoding,
        notify=selected_encoding_changed
    )

    # templates

    def get_templates(self) -> List[TemplateData]:
        return self.__templates

    def set_templates(self, value: List[TemplateData]):
        if self.templates != value:
            self.__templates = value
            self.templates_changed.emit(self.templates)

    templates = Property(
        type(List[TemplateData]),
        fget=get_templates,
        fset=set_templates,
        notify=templates_changed
    )

    # selected_template

    def get_selected_template(self) -> int:
        return self.__selected_template

    def set_selected_template(self, value: int):
        if self.selected_template != value:
            self.__selected_template = value
            self.selected_template_changed.emit(self.selected_template)

    selected_template = Property(
        int,
        fget=get_selected_template,
        fset=set_selected_template,
        notify=selected_template_changed
    )

    def initialize(self):
        self.encodings = EditDocumentTasks.get_encodings()
        self.selected_encoding = 0 if len(self.encodings) == 0 else self.encodings[0].id
        self.templates = EditTemplateTasks.get_templates()
        self.selected_template = 0 if len(self.templates) == 0 else self.templates[0].id
