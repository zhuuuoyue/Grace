# -*- coding: utf-8 -*-

import re
from typing import Optional, Set, Tuple

from PySide6.QtCore import QObject, Signal, Slot, Property

from .CreationTemplateEditorModel import CreationTemplateEditorModel

_CONFIRM_BUTTON_TEXT_OK = r'确定'
_CONFIRM_BUTTON_TEXT_EMPTY = r'模板名称不能为空'
_CONFIRM_BUTTON_TEXT_DUPLICATED = r'模板名称已存在'
_CONFIRM_BUTTON_CSS_VALID = r'QPushButton { color: black; }'
_CONFIRM_BUTTON_CSS_INVALID = r'QPushButton { color: red; }'

_PARAMETER_PATTERN = re.compile(r'\$\{(\w[\w\d]*)\}')


class CreationTemplateEditorViewModel(QObject):

    name_text_changed = Signal(str)
    content_text_changed = Signal(str)
    parameters_text_changed = Signal(str)
    confirm_enabled_changed = Signal(bool)
    confirm_text_changed = Signal(str)
    confirm_css_changed = Signal(str)

    def __init__(self, existing_template_names: Set[str], parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__existing_template_names: Set[str] = existing_template_names
        self.__model = CreationTemplateEditorModel(self)

        # attributes
        self.__name_text: str = str()
        self.__content_text: str = str()
        self.__parameters_text: str = str()
        self.__confirm_enabled: bool = False
        self.__confirm_text: str = _CONFIRM_BUTTON_TEXT_EMPTY
        self.__confirm_css: str = _CONFIRM_BUTTON_CSS_INVALID

        # connection
        self.__model.name_changed.connect(self.on_model_name_changed)
        self.__model.content_changed.connect(self.on_model_content_changed)

    @property
    def model(self) -> CreationTemplateEditorModel:
        return self.__model

    def get_name_text(self) -> str:
        return self.__name_text

    def set_name_text(self, value: str):
        if value != self.name_text:
            self.__name_text = value
            self.name_text_changed.emit(self.name_text)

    name_text = Property(str, fget=get_name_text, fset=set_name_text, notify=name_text_changed)

    def get_content_text(self) -> str:
        return self.__content_text

    def set_content_text(self, value: str):
        if value != self.content_text:
            self.__content_text = value
            self.content_text_changed.emit(self.content_text)

    content_text = Property(str, fget=get_content_text, fset=set_content_text, notify=content_text_changed)

    def get_parameters_text(self) -> str:
        return self.__parameters_text

    def set_parameters_text(self, value: str):
        if value != self.parameters_text:
            self.__parameters_text = value
            self.parameters_text_changed.emit(self.parameters_text)

    parameters_text = Property(str, fget=get_parameters_text, fset=set_parameters_text, notify=parameters_text_changed)

    def get_confirm_enabled(self) -> bool:
        return self.__confirm_enabled

    def set_confirm_enabled(self, value: bool):
        if value != self.confirm_enabled:
            self.__confirm_enabled = value
            self.confirm_enabled_changed.emit(self.confirm_enabled)

    confirm_enabled = Property(str, fget=get_confirm_enabled, fset=set_confirm_enabled, notify=confirm_enabled_changed)

    def get_confirm_text(self) -> str:
        return self.__confirm_text

    def set_confirm_text(self, value: str):
        if self.confirm_text != value:
            self.__confirm_text = value
            self.confirm_text_changed.emit(self.confirm_text)

    confirm_text = Property(str, fget=get_confirm_text, fset=set_confirm_text, notify=confirm_text_changed)

    def get_confirm_css(self) -> str:
        return self.__confirm_css

    def set_confirm_css(self, value: str):
        if self.confirm_css != value:
            self.__confirm_css = value
            self.confirm_css_changed.emit(self.confirm_css)

    confirm_css = Property(str, fget=get_confirm_css, fset=set_confirm_css, notify=confirm_css_changed)

    @Slot(str)
    def on_model_name_changed(self, name: str):
        self.name_text = name
        valid, message = self.__validate_template_name(name)
        if valid:
            self.confirm_enabled = True
            self.confirm_text = _CONFIRM_BUTTON_TEXT_OK
            self.confirm_css = _CONFIRM_BUTTON_CSS_VALID
        else:
            self.confirm_enabled = False
            self.confirm_text = message
            self.confirm_css = _CONFIRM_BUTTON_CSS_INVALID

    @Slot(str)
    def on_model_content_changed(self, content: str):
        self.content_text = content
        result = re.findall(_PARAMETER_PATTERN, content)
        self.parameters_text = ', '.join(set(result))

    # public

    def set_name(self, value: str):
        self.__model.set_name(value)

    def set_content(self, value: str):
        self.__model.set_content(value)

    # private

    def __validate_template_name(self, name: str) -> Tuple[bool, str]:
        if len(name) == 0:
            return False, _CONFIRM_BUTTON_TEXT_EMPTY
        if name in self.__existing_template_names:
            return False, _CONFIRM_BUTTON_TEXT_DUPLICATED
        return True, f''
