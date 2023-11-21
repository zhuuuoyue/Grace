# -*- coding: utf-8 -*-

from typing import Optional, Set

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QDialog

from .CreationSolutionEditorView import CreationSolutionEditorView


class CreationSolutionEditorDialog(QDialog):

    def __init__(self, existing_solution_names: Optional[Set[str]] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__ui = CreationSolutionEditorView(self)
        self.__existing_solution_names: Set[str] = set() if existing_solution_names is None else existing_solution_names

        self.__ui.input.textChanged.connect(self.__on_input_text_changed)
        self.__ui.confirm.clicked.connect(self.__on_confirm_button_clicked)

        self.__initialize()

    def get_solution_name(self) -> str:
        return self.__ui.input.text()

    @Slot(str)
    def __on_input_text_changed(self, text: str):
        if len(text) == 0:
            return self.__update_confirm_button(False, r'创建方案名称不能为空', 'color: red;')
        if text in self.__existing_solution_names:
            return self.__update_confirm_button(False, r'创建方案名称已存在', 'color: red;')
        self.__update_confirm_button(True, r'确定', 'color: black;')

    @Slot()
    def __on_confirm_button_clicked(self):
        self.accept()

    def __update_confirm_button(self, enabled: bool, text: str, css: str):
        self.__ui.confirm.setEnabled(enabled)
        self.__ui.confirm.setText(text)
        self.__ui.confirm.setStyleSheet(css)

    def __initialize(self):
        self.__on_input_text_changed('')
