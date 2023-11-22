# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from tasks.create import EditTemplateTasks

from ui.base import DialogBase

from .EditCreationTemplatesView import EditCreationTemplatesView
from .EditCreationTemplatesViewModel import EditCreationTemplatesViewModel
from app.create.CreationTemplateEditor import CreationTemplateEditor


class EditCreationTemplatesDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(object_name='491d3fc2-1bd1-485c-bb62-ebd27a45dd7e', parent=parent)
        self.vm = EditCreationTemplatesViewModel(self)
        self.ui = EditCreationTemplatesView(self, self.vm)

        self.ui.template_list.clicked.connect(self.vm.set_current_template_index)
        self.ui.new_button.clicked.connect(self.__on_new_button_clicked)
        self.ui.remove_button.clicked.connect(self.__on_remove_button_clicked)
        self.ui.edit_button.clicked.connect(self.__on_edit_button_clicked)
        self.ui.copy_button.clicked.connect(self.__on_copy_button_clicked)
        self.ui.export_button.clicked.connect(self.__on_export_button_clicked)
        self.ui.import_button.clicked.connect(self.__on_import_button_clicked)

        self.vm.current_template_index_changed.connect(self.ui.template_list.setCurrentIndex)
        self.vm.template_preview_text_changed.connect(self.ui.template_preview.setText)
        self.vm.new_button_enabled_changed.connect(self.ui.new_button.setEnabled)
        self.vm.remove_button_enabled_changed.connect(self.ui.remove_button.setEnabled)
        self.vm.edit_button_enabled_changed.connect(self.ui.edit_button.setEnabled)
        self.vm.copy_button_enabled_changed.connect(self.ui.copy_button.setEnabled)
        self.vm.export_button_enabled_changed.connect(self.ui.export_button.setEnabled)
        self.vm.import_button_enabled_changed.connect(self.ui.import_button.setEnabled)

    def initialize(self):
        self.vm.initialize()

    @Slot()
    def __on_new_button_clicked(self):
        editor = CreationTemplateEditor(existing_template_names={'cpp', 'python'}, parent=self)
        if 1 == editor.exec():
            new_template = editor.get_data()
            EditTemplateTasks.add_template(new_template)
            self.vm.model.update()

    @Slot()
    def __on_remove_button_clicked(self):
        current_template = self.vm.get_current_template_data()
        if current_template is not None:
            EditTemplateTasks.delete_template(current_template.name)
            self.vm.model.update()

    @Slot()
    def __on_edit_button_clicked(self):
        current_template_data = self.vm.get_current_template_data()
        if current_template_data is None:
            return

        current_template_name = current_template_data.name
        existing_template_names = EditTemplateTasks.get_template_names()
        existing_template_names.remove(current_template_name)
        editor = CreationTemplateEditor(
            existing_template_names=existing_template_names,
            data=current_template_data,
            parent=self
        )
        if 1 == editor.exec():
            modified_template = editor.get_data()
            EditTemplateTasks.update_template(current_template_name, modified_template)
            self.vm.model.update()

    @Slot()
    def __on_copy_button_clicked(self):
        source_template_data = self.vm.get_current_template_data()
        if source_template_data is not None:
            EditTemplateTasks.copy_and_insert_template(source_template_data)
            self.vm.model.update()

    @Slot()
    def __on_export_button_clicked(self):
        print('export')

    @Slot()
    def __on_import_button_clicked(self):
        print('import')
