# -*- coding: utf-8 -*-

import os
from typing import List, Optional

from PySide6.QtCore import QObject, Signal, Slot


class DirectoryInformation(object):

    def __init__(self, dir_path: str, checked: bool):
        self.path: str = dir_path
        self.checked: bool = checked

    def __eq__(self, other) -> bool:
        if not isinstance(other, DirectoryInformation):
            return False
        return self.path == other.path and self.checked == other.checked


class CleanLogFilesViewModel(QObject):

    repositories_changed = Signal()
    repository_changed = Signal(int)
    configurations_changed = Signal()
    configuration_changed = Signal(int)
    directories_changed = Signal()
    clean_button_text_changed = Signal(str)
    clean_button_enabled_changed = Signal(bool)
    directory_check_state_changed = Signal(int)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__repositories: List[str] = []
        self.__repository: int = -1
        self.__configurations: List[str] = []
        self.__configuration: int = -1
        self.__directories: List[DirectoryInformation] = []
        self.__clean_button_text: str = 'Clean'
        self.__clean_button_enabled: bool = False

        self.directories_changed.connect(self.update_clean_button_enabled_state)
        self.directory_check_state_changed.connect(self.on_clean_list_item_check_state_changed)

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
        if self.repositories != value:
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
    def configurations(self, value: List[str]):
        if self.configurations != value:
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
        if self.directories != value:
            self.__directories = value
            self.directories_changed.emit()

    def update_directories(self):
        if self.repository < 0 or self.repository >= len(self.repositories):
            return
        if self.configuration < 0 or self.configuration >= len(self.configurations):
            return
        repo = self.repositories[self.repository]
        config = self.configurations[self.configuration]
        config_mapping = {
            "Q_Debug": "x64Q_Debug",
            "Debug": "x64Debug",
        }
        if config in config_mapping:
            config_dir = config_mapping[config]
            output_dir = os.path.join(repo, 'bin', config_dir)
            self.directories = [
                DirectoryInformation(os.path.join(output_dir, 'Logs'), False),
                DirectoryInformation(os.path.join(output_dir, 'sdk', 'Logs'), False),
            ]

    def set_directory_check_state(self, index: int, checked: bool):
        if not isinstance(index, int) or not isinstance(checked, bool):
            return
        if index < 0 or index >= len(self.directories):
            return
        if self.directories[index].checked == checked:
            return
        self.directories[index].checked = checked
        self.directory_check_state_changed.emit(index)

    @property
    def clean_button_text(self) -> str:
        return self.__clean_button_text

    @clean_button_text.setter
    def clean_button_text(self, value: str):
        if isinstance(value, str) and value != self.clean_button_text:
            self.__clean_button_text = value
            self.clean_button_text_changed.emit(self.clean_button_text)

    def start_cleaning(self):
        self.clean_button_text = 'Cleaning'

    def end_cleaning(self):
        self.clean_button_text = 'Clean'

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
    def on_clean_list_item_check_state_changed(self, index: int):
        self.update_clean_button_enabled_state()
