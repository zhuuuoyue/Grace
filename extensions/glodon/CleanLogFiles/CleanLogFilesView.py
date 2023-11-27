# -*- coding: utf-8 -*-

from typing import List

from PySide6.QtCore import Qt, QSignalBlocker
from PySide6.QtWidgets import QDialog, QComboBox, QListWidget, QListWidgetItem

from ui.utils import create_no_focus_button, create_row_title, create_row_layout, create_column_layout

from .CleanLogFilesViewModel import CleanLogFilesViewModel, DirectoryInformation


class CleanLogFilesView(object):

    def __init__(self, dialog: QDialog, vm: CleanLogFilesViewModel):
        dialog.setFixedSize(600, 200)

        self.repository_title = create_row_title('Repository', width=100)
        self.repository_selector = QComboBox()
        self.update_repositories(vm.repositories, vm.repository)
        self.repository_row = create_row_layout(self.repository_selector, title=self.repository_title)

        self.configuration_title = create_row_title('Configuration', width=100)
        self.configuration_selector = QComboBox()
        self.update_configurations(vm.configurations, vm.configuration)
        self.configuration_row = create_row_layout(self.configuration_selector, title=self.configuration_title)

        self.clean_list_title = create_row_title('Clean List', width=100)
        self.clean_list = QListWidget()
        self.update_clean_list(vm.directories)
        self.clean_list_row = create_row_layout(self.clean_list, title=self.clean_list_title)
        self.clean_list_row.setAlignment(self.clean_list_title, Qt.AlignmentFlag.AlignTop)

        self.clean_button = create_no_focus_button(vm.clean_button_text)
        self.clean_button.setEnabled(vm.clean_button_enabled)

        self.layout = create_column_layout([
            self.repository_row, self.configuration_row, self.clean_list_row, self.clean_button
        ])
        self.layout.setContentsMargins(8, 8, 8, 8)

        dialog.setLayout(self.layout)
        dialog.setStyleSheet('QWidget { font-family: \'Consolas\'; }')

    def update_repositories(self, repositories: List[str], current_index: int):
        blocker = QSignalBlocker(self.repository_selector)
        self.repository_selector.clear()
        self.repository_selector.addItems(repositories)
        self.repository_selector.setCurrentIndex(current_index)
        blocker.unblock()

    def update_configurations(self, configurations: List[str], current_index: int):
        blocker = QSignalBlocker(self.configuration_selector)
        self.configuration_selector.clear()
        self.configuration_selector.addItems(configurations)
        self.configuration_selector.setCurrentIndex(current_index)
        blocker.unblock()

    def update_clean_list(self, dirs: List[DirectoryInformation]):
        blocker = QSignalBlocker(self.clean_list)
        self.clean_list.clear()
        for item_dir in dirs:
            item = QListWidgetItem(item_dir.path)
            item.setCheckState(Qt.CheckState.Checked if item_dir.checked else Qt.CheckState.Unchecked)
            self.clean_list.addItem(item)
        blocker.unblock()
