# -*- coding: utf-8 -*-

from typing import Optional, List

from PySide6.QtCore import QObject, Slot, Signal, Property, QSize

from tasks.create import TemplateData, Encoding

from .CreationDocumentEditorModel import CreationDocumentEditorModel


_CONFIRM_TEXT_EMPTY_RELATIVE_PATH = r'文档路径为空'
_CONFIRM_TEXT_INVALID_RELATIVE_PATH = r'文档路径无效'
_CONFIRM_TEXT_RELATIVE_PATH_EXISTS = r'文档路径已存在'
_CONFIRM_TEXT_OK = r'确定'
_CONFIRM_TEXT_NO_ENCODING = r'未指定文件编码'
_CONFIRM_TEXT_NO_TEMPLATE = r'未指定文档模板'
_CONFIRM_STYLE_SHEET_ENABLED = r'color: black;'
_CONFIRM_STYLE_SHEET_NOT_ENABLED = r'color: red;'


class CreationDocumentEditorViewModel(QObject):

    dialog_size_changed = Signal(QSize)
    relative_path_text_changed = Signal(str)
    encoding_list_changed = Signal(type(List[str]))
    encoding_index_changed = Signal(int)
    template_list_changed = Signal(type(List[str]))
    template_index_changed = Signal(int)
    template_preview_text_changed = Signal(str)
    template_preview_hidden_changed = Signal(bool)
    template_preview_size_changed = Signal(QSize)
    confirm_button_text_changed = Signal(str)
    confirm_button_enabled_changed = Signal(bool)
    confirm_button_style_sheet_changed = Signal(str)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

        self.__model = CreationDocumentEditorModel(self)

        self.__dialog_size: QSize = QSize()
        self.__relative_path_text: str = str()
        self.__encoding_list: List[str] = list()
        self.__encoding_index: int = -1
        self.__template_list: List[str] = list()
        self.__template_index: int = -1
        self.__template_preview_text: str = str()
        self.__template_preview_hidden: bool = False
        self.__template_preview_size: QSize = QSize()
        self.__confirm_button_text: str = _CONFIRM_TEXT_EMPTY_RELATIVE_PATH
        self.__confirm_button_enabled: bool = False
        self.__confirm_button_style_sheet: str = _CONFIRM_STYLE_SHEET_NOT_ENABLED

        self.template_preview_hidden_changed.connect(self.__on_template_preview_hidden_changed)

        self.__model.encodings_changed.connect(self.__on_encodings_changed)
        self.__model.selected_encoding_changed.connect(self.__on_selected_encoding_changed)
        self.__model.templates_changed.connect(self.__on_templates_changed)
        self.__model.selected_template_changed.connect(self.__on_selected_template_changed)

    # model

    def get_model(self) -> CreationDocumentEditorModel:
        return self.__model

    model = property(fget=get_model)

    # dialog_size

    def get_dialog_size(self) -> QSize:
        return self.__dialog_size

    def set_dialog_size(self, value: QSize):
        if self.dialog_size != value:
            self.__dialog_size = value
            self.dialog_size_changed.emit(self.dialog_size)

    dialog_size = Property(QSize, fget=get_dialog_size, fset=set_dialog_size, notify=dialog_size_changed)

    # relative_path

    def get_relative_path_text(self) -> str:
        return self.__relative_path_text

    @Slot(str)
    def set_relative_path_text(self, value: str):
        if self.relative_path_text != value:
            self.__relative_path_text = value
            self.relative_path_text_changed.emit(self.relative_path_text)

    relative_path_text = Property(
        str,
        fget=get_relative_path_text,
        fset=set_relative_path_text,
        notify=relative_path_text_changed
    )

    # encoding_list

    def get_encoding_list(self) -> List[str]:
        return self.__encoding_list

    @Slot(type(List[str]))
    def set_encoding_list(self, value: List[str]):
        if self.encoding_list != value:
            self.__encoding_list = value
            self.encoding_list_changed.emit(self.encoding_list)

    encoding_list = Property(
        type(List[str]),
        fget=get_encoding_list,
        fset=set_encoding_list,
        notify=encoding_list_changed
    )

    # encoding_index

    def get_encoding_index(self) -> int:
        return self.__encoding_index

    def set_encoding_index(self, value: int):
        if self.encoding_index != value:
            self.__encoding_index = value
            self.encoding_index_changed.emit(self.encoding_index)

    encoding_index = Property(
        int,
        fget=get_encoding_index,
        fset=set_encoding_index,
        notify=encoding_index_changed
    )

    # template_list

    def get_template_list(self) -> List[str]:
        return self.__template_list

    @Slot(type(List[str]))
    def set_template_list(self, value: List[str]):
        if self.template_list != value:
            self.__template_list = value
            self.template_list_changed.emit(self.template_list)

    template_list = Property(
        type(List[str]),
        fget=get_template_list,
        fset=set_template_list,
        notify=template_list_changed
    )

    # template_index

    def get_template_index(self) -> int:
        return self.__template_index

    def set_template_index(self, value: int):
        if self.template_index != value:
            self.__template_index = value
            self.template_index_changed.emit(self.template_index)

    template_index = Property(
        int,
        fget=get_template_index,
        fset=set_template_index,
        notify=template_index_changed
    )

    # template_preview_text

    def get_template_preview_text(self) -> str:
        return self.__template_preview_text

    @Slot(str)
    def set_template_preview_text(self, value: str):
        if self.template_preview_text != value:
            self.__template_preview_text = value
            self.template_preview_text_changed.emit(self.template_preview_text)

    template_preview_text = Property(
        str,
        fget=get_template_preview_text,
        fset=set_template_preview_text,
        notify=template_preview_text_changed
    )

    # template_preview_hidden

    def get_template_preview_hidden(self) -> bool:
        return self.__template_preview_hidden

    @Slot(str)
    def set_template_preview_hidden(self, value: bool):
        if self.template_preview_hidden != value:
            self.__template_preview_hidden = value
            self.template_preview_hidden_changed.emit(self.template_preview_hidden)

    template_preview_hidden = Property(
        bool,
        fget=get_template_preview_hidden,
        fset=set_template_preview_hidden,
        notify=template_preview_hidden_changed
    )

    # template_preview_size

    def get_template_preview_size(self) -> QSize:
        return self.__template_preview_size

    def set_template_preview_size(self, value: QSize):
        if self.template_preview_size != value:
            self.__template_preview_size = value
            self.template_preview_size_changed.emit(self.template_preview_size)

    template_preview_size = Property(
        QSize,
        fget=get_template_preview_size,
        fset=set_template_preview_size,
        notify=template_preview_size_changed
    )

    # confirm_button_text

    def get_confirm_button_text(self) -> str:
        return self.__confirm_button_text

    @Slot(str)
    def set_confirm_button_text(self, value: str):
        if self.confirm_button_text != value:
            self.__confirm_button_text = value
            self.confirm_button_text_changed.emit(self.confirm_button_text)

    confirm_button_text = Property(
        str,
        fget=get_confirm_button_text,
        fset=set_confirm_button_text,
        notify=confirm_button_text_changed
    )

    # confirm_button_enabled

    def get_confirm_button_enabled(self) -> bool:
        return self.__confirm_button_enabled

    @Slot(str)
    def set_confirm_button_enabled(self, value: bool):
        if self.confirm_button_enabled != value:
            self.__confirm_button_enabled = value
            self.confirm_button_enabled_changed.emit(self.confirm_button_enabled)

    confirm_button_enabled = Property(
        bool,
        fget=get_confirm_button_enabled,
        fset=set_confirm_button_enabled,
        notify=confirm_button_enabled_changed
    )

    # confirm_button_style_sheet

    def get_confirm_button_style_sheet(self) -> str:
        return self.__confirm_button_style_sheet

    @Slot(str)
    def set_confirm_button_style_sheet(self, value: str):
        if self.confirm_button_style_sheet != value:
            self.__confirm_button_style_sheet = value
            self.confirm_button_style_sheet_changed.emit(self.confirm_button_style_sheet)

    confirm_button_style_sheet = Property(
        str,
        fget=get_confirm_button_style_sheet,
        fset=set_confirm_button_style_sheet,
        notify=confirm_button_style_sheet_changed
    )

    # public

    @Slot()
    def switch_template_preview_hidden_state(self):
        self.template_preview_hidden = not self.template_preview_hidden

    @Slot()
    def update_confirm_button_state(self):
        pass

    # slots

    @Slot(QSize)
    def __on_template_preview_hidden_changed(self, hidden: bool):
        old_dialog_size = self.get_dialog_size()
        new_dialog_size = QSize(old_dialog_size.width(), old_dialog_size.height())
        if hidden:
            new_dialog_size.setHeight(new_dialog_size.height() - self.get_template_preview_size().height() - 8)
        else:
            new_dialog_size.setHeight(new_dialog_size.height() + self.get_template_preview_size().height() + 8)
        self.dialog_size = new_dialog_size

    @Slot(type(List[Encoding]))
    def __on_encodings_changed(self, encodings: List[Encoding]):
        self.encoding_list = [item.name for item in encodings]

    @Slot(int)
    def __on_selected_encoding_changed(self, encoding_id: int):
        for encoding_index, encoding in enumerate(self.model.encodings):
            if encoding.id == encoding_id:
                self.encoding_index = encoding_index

    @Slot(type(List[TemplateData]))
    def __on_templates_changed(self, templates: List[TemplateData]):
        self.template_list = [item.name for item in templates]

    @Slot(int)
    def __on_selected_template_changed(self, template_id: int):
        for template_index, template_data in enumerate(self.model.templates):
            if template_data.id == template_id:
                self.template_index = template_index
