# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QWidget

from .EditTemplateView import EditTemplateView
from .EditTemplateViewModel import EditTemplateViewModel
from .TemplateEditor import TemplateEditor


class EditTemplateDialog(QDialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.vm = EditTemplateViewModel(self)
        self.ui = EditTemplateView(self, self.vm)

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
        editor = TemplateEditor(existing_template_names={'cpp', 'python'}, parent=self)
        if 1 == editor.exec():
            new_template = editor.get_data()
            print('will add template')
            print(new_template)

    @Slot()
    def __on_remove_button_clicked(self):
        print('remove')

    @Slot()
    def __on_edit_button_clicked(self):
        editor = TemplateEditor(existing_template_names={'cpp', 'python'}, parent=self)
        if 1 == editor.exec():
            modified_template = editor.get_data()
            print('will modify template')
            print(modified_template)

    @Slot()
    def __on_copy_button_clicked(self):
        print('copy')

    @Slot()
    def __on_export_button_clicked(self):
        print('export')

    @Slot()
    def __on_import_button_clicked(self):
        print('import')
