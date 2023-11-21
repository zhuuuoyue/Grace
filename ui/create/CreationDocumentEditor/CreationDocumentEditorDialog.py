# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Optional

from PySide6.QtCore import Slot, QSize, QSignalBlocker
from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtGui import QResizeEvent

from .CreationDocumentEditorView import CreationDocumentEditorView
from .CreationDocumentEditorViewModel import CreationDocumentEditorViewModel


class CreationDocumentEditorDialog(QDialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__ui = CreationDocumentEditorView(self)
        self.__vm = CreationDocumentEditorViewModel(self)
        self.__load_data()

        self.__vm.dialog_size_changed.connect(self.__on_dialog_size_changed)
        self.__vm.encoding_list_changed.connect(self.__ui.encoding_selector.addItems)
        self.__vm.encoding_index_changed.connect(self.__ui.encoding_selector.setCurrentIndex)
        self.__vm.template_list_changed.connect(self.__ui.template_selector.addItems)
        self.__vm.template_index_changed.connect(self.__ui.template_selector.setCurrentIndex)
        self.__vm.template_preview_hidden_changed.connect(self.__ui.template_preview.setHidden)

        # self.__ui.preview_button.clicked.connect(self.__vm.switch_template_preview_hidden_state)  # bug

        self.resize(400, 600)

        self.__vm.model.initialize()

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        self.__vm.dialog_size = self.size()
        self.__vm.template_preview_size = self.__ui.template_preview.size()

    def __load_data(self):
        self.__ui.relative_path_input.setText(self.__vm.relative_path_text)
        self.__ui.encoding_selector.addItems(self.__vm.encoding_list)
        self.__ui.encoding_selector.setCurrentIndex(self.__vm.encoding_index)
        self.__ui.template_selector.addItems(self.__vm.template_list)
        self.__ui.template_selector.setCurrentIndex(self.__vm.template_index)
        self.__ui.template_preview.setText(self.__vm.template_preview_text)
        self.__ui.template_preview.setHidden(self.__vm.template_preview_hidden)
        self.__ui.confirm_button.setText(self.__vm.confirm_button_text)
        self.__ui.confirm_button.setStyleSheet(self.__vm.confirm_button_style_sheet)
        self.__ui.confirm_button.setEnabled(self.__vm.confirm_button_enabled)

    @Slot(QSize)
    def __on_dialog_size_changed(self, value: QSize):
        self.resize(value)
