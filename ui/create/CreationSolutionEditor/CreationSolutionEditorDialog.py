# -*- coding: utf-8 -*-

from typing import Optional, Set

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QDialog

from .CreationSolutionEditorView import CreationSolutionEditorView


class CreationSolutionEditorDialog(QDialog):

    def __init__(self, existing_name: Optional[Set[str]] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui = CreationSolutionEditorView(self)
        self.existing_name: Set[str] = set() if existing_name is None else existing_name

        self.ui.input.textChanged.connect(self.__on_input_text_changed)
        self.ui.confirm.clicked.connect(self.__on_confirm_button_clicked)

        self.__initialize()

    @Slot(str)
    def __on_input_text_changed(self, text: str):
        if len(text) == 0:
            return self.__update_confirm_button(False, r'创建方案名称不能为空', 'color: red;')
        if text in self.existing_name:
            return self.__update_confirm_button(False, r'创建方案名称已存在', 'color: red;')
        self.__update_confirm_button(True, r'确定', 'color: black;')

    @Slot()
    def __on_confirm_button_clicked(self):
        self.accept()

    def __update_confirm_button(self, enabled: bool, text: str, css: str):
        self.ui.confirm.setEnabled(enabled)
        self.ui.confirm.setText(text)
        self.ui.confirm.setStyleSheet(css)

    def __initialize(self):
        self.__on_input_text_changed('')
