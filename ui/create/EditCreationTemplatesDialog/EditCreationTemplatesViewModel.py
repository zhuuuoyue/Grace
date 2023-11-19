# -*- coding: utf-8 -*-

from typing import Optional, Dict, Union

from PySide6.QtCore import QObject, Property, Slot, Signal, QStringListModel, QModelIndex

from tasks.create import TemplateData

from .EditCreationTemplatesModel import EditCreationTemplatesModel


class EditCreationTemplatesViewModel(QObject):

    new_button_enabled_changed = Signal(bool)
    remove_button_enabled_changed = Signal(bool)
    edit_button_enabled_changed = Signal(bool)
    copy_button_enabled_changed = Signal(bool)
    export_button_enabled_changed = Signal(bool)
    import_button_enabled_changed = Signal(bool)
    current_template_index_changed = Signal(QModelIndex)
    template_preview_text_changed = Signal(str)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

        # model
        self.__model: EditCreationTemplatesModel = EditCreationTemplatesModel(self)
        self.__template_list_model = QStringListModel(self)

        # view model
        self.__new_button_enabled: bool = True
        self.__remove_button_enabled: bool = False
        self.__edit_button_enabled: bool = False
        self.__copy_button_enabled: bool = False
        self.__export_button_enabled: bool = False
        self.__import_button_enabled: bool = True

        self.__current_template_index: QModelIndex = self.create_index()
        self.__template_preview_text: str = str()

        # connection
        self.__model.data_changed.connect(self.__on_model_data_changed)
        self.current_template_index_changed.connect(self.__on_current_template_index_changed)

    def create_index(self, row: Optional[int] = -1) -> QModelIndex:
        return self.__template_list_model.createIndex(row, 0)

    def get_model(self) -> EditCreationTemplatesModel:
        return self.__model

    model = property(fget=get_model)

    def get_template_list_model(self) -> QStringListModel:
        return self.__template_list_model

    template_list_model = property(fget=get_template_list_model)

    def get_new_button_enabled(self) -> bool:
        return self.__new_button_enabled

    def set_new_button_enabled(self, value: bool):
        if self.__new_button_enabled != value:
            self.__new_button_enabled = value
            self.new_button_enabled_changed.emit(self.__new_button_enabled)

    new_button_enabled = Property(bool, fget=get_new_button_enabled, fset=set_new_button_enabled,
                                  notify=new_button_enabled_changed)

    def get_remove_button_enabled(self) -> bool:
        return self.__remove_button_enabled

    def set_remove_button_enabled(self, value: bool):
        if self.__remove_button_enabled != value:
            self.__remove_button_enabled = value
            self.remove_button_enabled_changed.emit(self.__remove_button_enabled)

    remove_button_enabled = Property(bool, fget=get_remove_button_enabled, fset=set_remove_button_enabled,
                                     notify=remove_button_enabled_changed)

    def get_edit_button_enabled(self) -> bool:
        return self.__edit_button_enabled

    def set_edit_button_enabled(self, value: bool):
        if self.__edit_button_enabled != value:
            self.__edit_button_enabled = value
            self.edit_button_enabled_changed.emit(self.__edit_button_enabled)

    edit_button_enabled = Property(bool, fget=get_edit_button_enabled, fset=set_edit_button_enabled,
                                  notify=edit_button_enabled_changed)

    def get_copy_button_enabled(self) -> bool:
        return self.__copy_button_enabled

    def set_copy_button_enabled(self, value: bool):
        if self.__copy_button_enabled != value:
            self.__copy_button_enabled = value
            self.copy_button_enabled_changed.emit(self.__copy_button_enabled)

    copy_button_enabled = Property(bool, fget=get_copy_button_enabled, fset=set_copy_button_enabled,
                                  notify=copy_button_enabled_changed)

    def get_export_button_enabled(self) -> bool:
        return self.__export_button_enabled

    def set_export_button_enabled(self, value: bool):
        if self.__export_button_enabled != value:
            self.__export_button_enabled = value
            self.export_button_enabled_changed.emit(self.__export_button_enabled)

    export_button_enabled = Property(bool, fget=get_export_button_enabled, fset=set_export_button_enabled,
                                  notify=export_button_enabled_changed)

    def get_import_button_enabled(self) -> bool:
        return self.__import_button_enabled

    def set_import_button_enabled(self, value: bool):
        if self.__import_button_enabled != value:
            self.__import_button_enabled = value
            self.import_button_enabled_changed.emit(self.__import_button_enabled)

    import_button_enabled = Property(bool, fget=get_import_button_enabled, fset=set_import_button_enabled,
                                  notify=import_button_enabled_changed)

    def get_template_preview_text(self) -> str:
        return self.__template_preview_text

    def set_template_preview_text(self, value: str):
        if self.__template_preview_text != value:
            self.__template_preview_text = value
            self.template_preview_text_changed.emit(self.__template_preview_text)

    template_preview_text = Property(str, fget=get_template_preview_text, fset=set_template_preview_text,
                                     notify=template_preview_text_changed)

    def get_current_template_index(self) -> QModelIndex:
        return self.__current_template_index

    def set_current_template_index(self, value: QModelIndex):
        if self.__current_template_index != value:
            self.__current_template_index = value
            self.current_template_index_changed.emit(self.__current_template_index)

    current_template_index = Property(QModelIndex, fget=get_current_template_index, fset=set_current_template_index,
                                      notify=current_template_index_changed)

    def initialize(self):
        self.__model.initialize()

    @Slot(type(Dict[str, str]))
    def __on_model_data_changed(self, data: Dict[str, str]):
        old_template_name_list = self.__template_list_model.stringList()
        old_current_template_name = str()
        current_template_index: int = self.get_current_template_index().row()
        if 0 <= current_template_index < len(old_template_name_list):
            old_current_template_name = old_template_name_list[current_template_index]
        new_template_name_list = data.keys()

        self.current_template_index = self.create_index()
        self.__template_list_model.beginResetModel()
        self.__template_list_model.setStringList(new_template_name_list)
        self.__template_list_model.endResetModel()

        if len(old_current_template_name) != 0:
            for new_current_template_index, new_template_name in enumerate(new_template_name_list):
                if new_template_name == old_current_template_name:
                    self.current_template_index = self.create_index(new_current_template_index)

        if self.current_template_index.row() < 0 < len(new_template_name_list):
            self.current_template_index = self.create_index(0)

    @Slot(QModelIndex)
    def __on_current_template_index_changed(self, current_template_index: QModelIndex):
        template_name_list = list(self.__model.data.keys())
        current_template_index_value = current_template_index.row()
        if current_template_index_value < 0 or current_template_index_value >= len(template_name_list):
            self.new_button_enabled = True
            self.remove_button_enabled = False
            self.edit_button_enabled = False
            self.copy_button_enabled = False
            self.export_button_enabled = False
            self.import_button_enabled = True
        else:
            self.new_button_enabled = True
            self.remove_button_enabled = True
            self.edit_button_enabled = True
            self.copy_button_enabled = True
            self.export_button_enabled = True
            self.import_button_enabled = True

            current_template_name = template_name_list[current_template_index_value]
            template_content = self.__model.data[current_template_name]
            # to paint
            self.template_preview_text = template_content

    def get_current_template_data(self) -> Union[TemplateData, None]:
        current_template_index = self.current_template_index.row()
        template_name_list = self.template_list_model.stringList()
        if current_template_index < 0 or current_template_index >= len(template_name_list):
            return None
        current_template_name = template_name_list[current_template_index]
        current_template_content = self.model.get_content(current_template_name)
        if current_template_content is None:
            return None
        return TemplateData(name=current_template_name, content=current_template_content)
