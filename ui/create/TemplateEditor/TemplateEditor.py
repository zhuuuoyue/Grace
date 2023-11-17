# -*- coding: utf-8 -*-

from typing import Optional, Set

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialog, QWidget

from tasks.create import TemplateData

from .TemplateEditorViewModel import TemplateEditorViewModel
from .TemplateEditorView import TemplateEditorView


class TemplateEditor(QDialog):

    def __init__(self, existing_template_names: Set[str],
                 data: Optional[TemplateData] = None,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.vm = TemplateEditorViewModel(existing_template_names, self)
        self.ui = TemplateEditorView(self, self.vm)

        self.vm.name_text_changed.connect(self.on_vm_name_text_changed)
        self.vm.content_text_changed.connect(self.on_vm_content_text_changed)
        self.vm.parameters_text_changed.connect(self.ui.parameter_input.setPlainText)
        self.vm.confirm_enabled_changed.connect(self.ui.confirm_button.setEnabled)
        self.vm.confirm_text_changed.connect(self.ui.confirm_button.setText)
        self.vm.confirm_css_changed.connect(self.ui.confirm_button.setStyleSheet)

        self.ui.name_input.textChanged.connect(self.vm.set_name)
        self.ui.content_input.textChanged.connect(self.on_ui_content_input_text_changed)
        self.ui.confirm_button.clicked.connect(self.on_ui_confirm_button_clicked)

        if data is not None:
            self.vm.model.load_data(data)

    def get_data(self) -> TemplateData:
        return self.vm.model.get_data()

    @Slot()
    def on_ui_content_input_text_changed(self):
        self.vm.set_content(self.ui.content_input.toPlainText())

    @Slot()
    def on_ui_confirm_button_clicked(self):
        self.accept()

    @Slot(str)
    def on_vm_name_text_changed(self, value: str):
        if value != self.ui.name_input.text():
            self.ui.name_input.setText(value)

    @Slot(str)
    def on_vm_content_text_changed(self, value: str):
        if value != self.ui.content_input.toPlainText():
            self.ui.content_input.setPlainText(value)
