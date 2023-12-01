# -*- coding: utf-8 -*-

__all__ = ['SwitchEnvironmentDialogViewModel']

from typing import List, Optional, Union

from PySide6.QtCore import Signal, Slot, Property, QObject

from ui import WidgetViewModelBase

from extensions.glodon.environment import Environment

from .switch_environment_dialog_model import SwitchEnvironmentDialogModel
from .environment_option import EnvironmentOption


class SwitchEnvironmentDialogViewModel(WidgetViewModelBase):

    software_path_list_changed = Signal(type(List[str]))
    current_software_path_index_changed = Signal(int)
    environment_options_changed = Signal(type(List[EnvironmentOption]))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__model = SwitchEnvironmentDialogModel(self)
        self.__software_path_list: List[str] = list()
        self.__current_software_path_index: int = -1
        self.__environment_options: List[EnvironmentOption] = [
            EnvironmentOption(Environment.A, 'A', True),
            EnvironmentOption(Environment.B, 'B', True),
            EnvironmentOption(Environment.C, 'C', True),
            EnvironmentOption(Environment.QA, 'QA', True),
            EnvironmentOption(Environment.QA_STG, 'QA STG', True)
        ]

    def initialize(self):
        # connect
        self.model.software_path_list_changed.connect(self.__on_model_software_path_list_changed)
        self.model.current_software_path_changed.connect(self.__on_model_current_software_path_changed)
        self.model.current_environment_changed.connect(self.__on_model_current_environment_changed)
        # initialize members
        self.model.initialize()

    def update(self):
        self.model.update()

    @property
    def model(self) -> SwitchEnvironmentDialogModel:
        return self.__model

    def get_software_path_list(self) -> List[str]:
        return self.__software_path_list

    def set_software_path_list(self, items: List[str]):
        if self.software_path_list != items:
            self.__software_path_list = items
            self.software_path_list_changed.emit(self.software_path_list)

    software_path_list = Property(
        type(List[str]),
        fget=get_software_path_list,
        fset=set_software_path_list,
        notify=software_path_list_changed
    )

    def get_current_software_path_index(self) -> int:
        return self.__current_software_path_index

    def set_current_software_path_index(self, value: int):
        if value != self.current_software_path_index:
            self.__current_software_path_index = value
            self.current_software_path_index_changed.emit(self.current_software_path_index)

    current_software_path_index = Property(
        int,
        fget=get_current_software_path_index,
        fset=set_current_software_path_index,
        notify=current_software_path_index_changed
    )

    def get_environment_options(self) -> List[EnvironmentOption]:
        return self.__environment_options

    def set_environment_options(self, opts: List[EnvironmentOption]):
        if self.environment_options != opts:
            self.__environment_options = opts
            self.environment_options_changed.emit(self.environment_options)

    environment_options = Property(
        type(List[EnvironmentOption]),
        fget=get_environment_options,
        fset=set_environment_options,
        notify=environment_options_changed
    )

    def request_switching_current_software(self, index: int):
        self.model.current_software_path = self.model.software_path_list[index]

    def request_updating_environment_options(self):
        self.model.update_current_software_environment()

    @Slot(type(List[str]))
    def __on_model_software_path_list_changed(self, software_path_list: List[str]):
        self.software_path_list = software_path_list

    @Slot(type(Union[str, None]))
    def __on_model_current_software_path_changed(self, current_software_path: Union[str, None]):
        if current_software_path is None:
            self.current_software_path_index = -1
        else:
            self.current_software_path_index = self.software_path_list.index(current_software_path)

    @Slot(type(Union[Environment, None]))
    def __on_model_current_environment_changed(self, current_environment: Union[Environment, None]):
        new_environment_options: List[EnvironmentOption] = [
            EnvironmentOption(Environment.A, 'A', True),
            EnvironmentOption(Environment.B, 'B', True),
            EnvironmentOption(Environment.C, 'C', True),
            EnvironmentOption(Environment.QA, 'QA', True),
            EnvironmentOption(Environment.QA_STG, 'QA STG', True)
        ]
        for new_environment_option in new_environment_options:
            if new_environment_option.environment == current_environment:
                new_environment_option.enabled = False
        self.environment_options = new_environment_options
