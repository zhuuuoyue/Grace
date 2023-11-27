# -*- coding: utf-8 -*-

from typing import Optional, List

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QListWidgetItem

from shared.utils import clean_directories
from ui.base import DialogBase

from .CleanLogFilesViewModel import CleanLogFilesViewModel
from .CleanLogFilesView import CleanLogFilesView


class CleanLogFilesDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(object_name='59d1f09f-9216-46d6-9d47-ef1b8a3cb217', parent=parent,
                         window_title='Clean Log Files')
        self.__vm = CleanLogFilesViewModel(self)
        self.__ui = CleanLogFilesView(self, self.__vm)

        self.__vm.repositories_changed.connect(self.__on_vm_repositories_changed)
        self.__vm.repository_changed.connect(self.__ui.repository_selector.setCurrentIndex)
        self.__vm.configurations_changed.connect(self.__on_vm_configurations_changed)
        self.__vm.configuration_changed.connect(self.__ui.configuration_selector.setCurrentIndex)
        self.__vm.directories_changed.connect(self.__on_vm_clean_list_changed)
        self.__vm.clean_button_enabled_changed.connect(self.__ui.clean_button.setEnabled)
        self.__vm.clean_button_text_changed.connect(
            self.__on_vm_clean_button_text_changed, Qt.ConnectionType.DirectConnection)

        self.__ui.repository_selector.currentIndexChanged.connect(self.__vm.set_repository)
        self.__ui.configuration_selector.currentIndexChanged.connect(self.__vm.set_configuration)
        self.__ui.clean_list.itemChanged.connect(self.__on_ui_clean_list_item_changed)
        self.__ui.clean_button.clicked.connect(self.__on_ui_clean_button_clicked)

        self.__vm.initialize()

    @Slot()
    def __on_vm_repositories_changed(self):
        self.__ui.update_repositories(self.__vm.repositories, self.__vm.repository)

    @Slot()
    def __on_vm_configurations_changed(self):
        self.__ui.update_configurations(self.__vm.configurations, self.__vm.configuration)

    @Slot()
    def __on_vm_clean_list_changed(self):
        self.__ui.update_clean_list(self.__vm.directories)

    @Slot(str)
    def __on_vm_clean_button_text_changed(self, text: str):
        self.__ui.clean_button.setText(text)
        self.__ui.clean_button.repaint()

    @Slot(QListWidgetItem)
    def __on_ui_clean_list_item_changed(self, item: QListWidgetItem):
        if not isinstance(item, QListWidgetItem):
            return
        index = self.__ui.clean_list.indexFromItem(item).row()
        checked = item.checkState() == Qt.CheckState.Checked
        self.__vm.set_directory_check_state(index, checked)

    @Slot()
    def __on_ui_clean_button_clicked(self):
        self.__vm.start_cleaning()
        dir_info_list = self.__vm.directories
        clean_list: List[str] = list()
        for dir_info in dir_info_list:
            if dir_info.checked:
                clean_list.append(dir_info.path)
        clean_directories(clean_list)
        self.__vm.end_cleaning()
