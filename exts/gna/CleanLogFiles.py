# -*- coding: utf-8 -*-

from typing import Optional, List, Any

from PySide6.QtCore import QObject, Qt, Slot, Signal, QSignalBlocker
from PySide6.QtWidgets import QWidget, QDialog, QLabel, QComboBox, QListWidgetItem, QListWidget

from common import is_string_list, are_same_string_lists, are_same_lists, is_list_of, FilterX
from command import ICommand
from ui.basic import form, create_no_focus_button
from .CleanDirectories import CleanDirectories


class DirectoryInformation(object):

    def __init__(self, dir_path: str, checked: bool):
        self.path: str = dir_path
        self.checked: bool = checked

    def __eq__(self, other) -> bool:
        if not isinstance(other, DirectoryInformation):
            return False
        return self.path == other.path and self.checked == other.checked


class IsDirectoryInformation(FilterX):

    def filter(self, obj: Any) -> bool:
        return isinstance(obj, DirectoryInformation)


class _VM(QObject):

    repositories_changed = Signal()
    repository_changed = Signal(int)
    configurations_changed = Signal()
    configuration_changed = Signal(int)
    directories_changed = Signal()
    clean_button_enabled_changed = Signal(bool)
    directory_checkable_changed = Signal(int)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__repositories: List[str] = []
        self.__repository: int = -1
        self.__configurations: List[str] = []
        self.__configuration: int = -1
        self.__directories: List[DirectoryInformation] = []
        self.__clean_button_enabled: bool = False

        self.directories_changed.connect(self.update_clean_button_enabled_state)
        self.directory_checkable_changed.connect(self.on_clean_list_item_checkable_changed)

    def initialize(self):
        self.repositories = ['D:\\gap', 'H:\\gap', 'I:\\gap']
        self.repository = 0
        self.configurations = ['Q_Debug', 'Debug']
        self.configuration = 0

    @property
    def repositories(self) -> List[str]:
        return self.__repositories

    @repositories.setter
    def repositories(self, value: List[str]):
        if not is_string_list(value):
            return
        if are_same_string_lists(self.repositories, value):
            return
        self.__repositories = value
        self.repositories_changed.emit()

    @property
    def repository(self) -> int:
        return self.__repository

    @repository.setter
    def repository(self, value: int):
        if isinstance(value, int) and 0 <= value < len(self.repositories) and self.repository != value:
            self.__repository = value
            self.repository_changed.emit(self.repository)

            self.update_directories()

    @Slot(int)
    def set_repository(self, repository: int):
        self.repository = repository

    @property
    def configurations(self) -> List[str]:
        return self.__configurations

    @configurations.setter
    def configurations(self, value):
        if not is_string_list(value):
            return
        if are_same_string_lists(self.configurations, value):
            return
        self.__configurations = value
        self.configurations_changed.emit()

    @property
    def configuration(self) -> int:
        return self.__configuration

    @configuration.setter
    def configuration(self, value: int):
        if isinstance(value, int) and 0 <= value < len(self.configurations) and value != self.configuration:
            self.__configuration = value
            self.configuration_changed.emit(self.configuration)

            self.update_directories()

    @Slot(int)
    def set_configuration(self, configuration: int):
        self.configuration = configuration

    @property
    def directories(self) -> List[DirectoryInformation]:
        return self.__directories

    @directories.setter
    def directories(self, value: List[DirectoryInformation]):
        if not is_list_of(value, IsDirectoryInformation()):
            return
        if are_same_lists(value, self.directories):
            return
        self.__directories = value
        self.directories_changed.emit()

    def update_directories(self):
        if self.repository < 0 or self.repository >= len(self.repositories):
            return
        if self.configuration < 0 or self.configuration >= len(self.configurations):
            return
        repo = self.repositories[self.repository]
        config = self.configurations[self.configuration]
        self.directories = [
            DirectoryInformation(f'{repo}\\bin\\{config}\\Logs', False),
            DirectoryInformation(f'{repo}\\bin\\{config}\\sdk\\Logs', False),
        ]

    def set_directory_check_state(self, index: int, checked: bool):
        if not isinstance(index, int) or not isinstance(checked, bool):
            return
        if index < 0 or index >= len(self.directories):
            return
        if self.directories[index].checked == checked:
            return
        self.directories[index].checked = checked
        self.directory_checkable_changed.emit(index)

    @property
    def clean_button_enabled(self) -> bool:
        return self.__clean_button_enabled

    @clean_button_enabled.setter
    def clean_button_enabled(self, value: bool):
        if isinstance(value, bool) and value != self.__clean_button_enabled:
            self.__clean_button_enabled = value
            self.clean_button_enabled_changed.emit(self.clean_button_enabled)

    @Slot()
    def update_clean_button_enabled_state(self):
        for dir_info in self.directories:
            if dir_info.checked:
                self.clean_button_enabled = True
                return
        self.clean_button_enabled = False

    @Slot(int)
    def on_clean_list_item_checkable_changed(self, index: int):
        self.update_clean_button_enabled_state()


class _UI(object):

    def __init__(self, dialog: QDialog, vm: _VM):
        dialog.setSizeGripEnabled(True)
        dialog.setFixedSize(600, 400)
        dialog.setWindowTitle('Clean Log Files')

        self.repository_title = form.create_row_title('Repository')
        self.repository_selector = QComboBox()
        self.update_repositories(vm.repositories, vm.repository)
        self.repository_row = form.create_row_layout(self.repository_selector, title=self.repository_title)

        self.configuration_title = form.create_row_title('Configuration')
        self.configuration_selector = QComboBox()
        self.update_configurations(vm.configurations, vm.configuration)
        self.configuration_row = form.create_row_layout(self.configuration_selector, title=self.configuration_title)

        self.clean_list_title = form.create_row_title('Clean List')
        self.clean_list = QListWidget()
        self.update_clean_list(vm.directories)
        self.clean_list_row = form.create_row_layout(self.clean_list, title=self.clean_list_title)
        self.clean_list_row.setAlignment(self.clean_list_title, Qt.AlignmentFlag.AlignTop)

        self.clean_button = create_no_focus_button('Clean')
        self.clean_button.setEnabled(vm.clean_button_enabled)

        self.layout = form.create_column_layout([
            self.repository_row, self.configuration_row, self.clean_list_row, self.clean_button
        ])
        self.layout.setContentsMargins(8, 8, 8, 8)

        dialog.setLayout(self.layout)

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


class CleanLogFilesDialog(QDialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__vm = _VM(self)
        self.__ui = _UI(self, self.__vm)

        self.__vm.repositories_changed.connect(self.__on_vm_repositories_changed)
        self.__vm.repository_changed.connect(self.__ui.repository_selector.setCurrentIndex)
        self.__vm.configurations_changed.connect(self.__on_vm_configurations_changed)
        self.__vm.configuration_changed.connect(self.__ui.configuration_selector.setCurrentIndex)
        self.__vm.directories_changed.connect(self.__on_vm_clean_list_changed)
        self.__vm.clean_button_enabled_changed.connect(self.__ui.clean_button.setEnabled)

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

    @Slot(QListWidgetItem)
    def __on_ui_clean_list_item_changed(self, item: QListWidgetItem):
        if not isinstance(item, QListWidgetItem):
            return
        index = self.__ui.clean_list.indexFromItem(item).row()
        checked = item.checkState() == Qt.CheckState.Checked
        self.__vm.set_directory_check_state(index, checked)

    @Slot()
    def __on_ui_clean_button_clicked(self):
        dir_info_list = self.__vm.directories
        clean_list: List[str] = list()
        for dir_info in dir_info_list:
            if dir_info.checked:
                clean_list.append(dir_info.path)
        cleaner = CleanDirectories(clean_list)
        cleaner.run()


class CleanLogFilesCommand(ICommand):

    def __init__(self):
        pass

    def exec(self, *args, **kwargs):
        dialog = CleanLogFilesDialog()
        dialog.exec()
