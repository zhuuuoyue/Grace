# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Any, Optional, Sequence, List

from PySide6.QtCore import QObject, Signal, Slot

from common.filter import FilterX
from common import is_list_of, are_same_lists

from ..utils import infer_environment, environment_to_string
from exts.gna.concept import Environment


class EnvironmentOption(object):

    def __init__(self, env: Environment, name: str, enabled: bool, checked: bool):
        self.environment: Environment = env
        self.name: str = name
        self.enabled: bool = enabled
        self.checked: bool = checked

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EnvironmentOption):
            return False
        return self.name == other.name and self.enabled == other.enabled and self.checked == other.checked


class IsEnvironmentOption(FilterX):

    def filter(self, obj: Any) -> bool:
        return isinstance(obj, EnvironmentOption)


class SwitchEnvironmentDialogViewModel(QObject):

    selected_software_changed = Signal()
    current_environment_changed = Signal(str)
    environment_options_changed = Signal()

    def __init__(self, packages: Sequence[str], parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__software_list: Sequence[str] = tuple()
        self.__selected_software: str = ''
        self.__current_environment: str = ''
        self.__environment_options: List[EnvironmentOption] = [
            EnvironmentOption(Environment.A, 'A', True, False),
            EnvironmentOption(Environment.B, 'B', True, False),
            EnvironmentOption(Environment.C, 'C', True, True),
            EnvironmentOption(Environment.QA, 'QA', False, False),
            EnvironmentOption(Environment.QA_STG, 'QA STG', True, False)
        ]

        self.selected_software_changed.connect(self.update_current_environment)
        self.current_environment_changed.connect(self.update_environment_options)

        self.initialize(packages)

    def initialize(self, packages: Sequence[str]):
        self.software_list = packages
        if len(self.software_list) > 0:
            self.selected_software = self.software_list[0]

    @property
    def software_list(self) -> Sequence[str]:
        return self.__software_list

    @software_list.setter
    def software_list(self, items: Sequence[str]):
        if isinstance(items, (list, tuple)):
            for item in items:
                if not isinstance(item, str):
                    return
            if len(items) == len(self.software_list):
                equal = True
                for a, b in zip(items, self.software_list):
                    if a != b:
                        equal = False
                        break
                if equal:
                    return
            self.__software_list = items

    @property
    def selected_software(self) -> str:
        return self.__selected_software

    @selected_software.setter
    def selected_software(self, value: str):
        if isinstance(value, str) and value != self.selected_software:
            self.__selected_software = value
            self.selected_software_changed.emit()

    @Slot(int)
    def set_selected_software_package(self, index: int):
        if 0 <= index < len(self.software_list):
            self.selected_software = self.software_list[index]

    @property
    def current_environment(self) -> str:
        return self.__current_environment

    @current_environment.setter
    def current_environment(self, value):
        value_str = value
        if not isinstance(value, str):
            value_str = environment_to_string(value)
        if isinstance(value_str, str) and value_str != self.current_environment:
            self.__current_environment = value_str
            self.current_environment_changed.emit(self.current_environment)

    @Slot()
    def update_current_environment(self):
        self.current_environment = infer_environment(self.selected_software)

    @property
    def environment_options(self) -> List[EnvironmentOption]:
        return self.__environment_options

    @environment_options.setter
    def environment_options(self, opts: List[EnvironmentOption]):
        if not is_list_of(opts, IsEnvironmentOption()):
            return
        if are_same_lists(self.environment_options, opts):
            return
        self.__environment_options = opts
        self.environment_options_changed.emit()

    @Slot(str)
    def update_environment_options(self, current_environment: str):
        new_env_opts: List[EnvironmentOption] = [
            EnvironmentOption(Environment.A, 'A', True, False),
            EnvironmentOption(Environment.B, 'B', True, False),
            EnvironmentOption(Environment.C, 'C', True, False),
            EnvironmentOption(Environment.QA, 'QA', True, False),
            EnvironmentOption(Environment.QA_STG, 'QA STG', True, False)
        ]
        current_environment_index: int = 0
        for index, env_opt in enumerate(new_env_opts):
            if env_opt.name == current_environment:
                env_opt.enabled = False
                current_environment_index = index
                break
        new_env_opts[(current_environment_index + 1) % len(new_env_opts)].checked = True
        self.environment_options = new_env_opts

    def set_environment_option_checked(self, env_name: str):
        new_env_opts = deepcopy(self.environment_options)
        for env_opt in new_env_opts:
            env_opt.checked = env_opt.name == env_name
        self.environment_options = new_env_opts

    def get_target_environment(self) -> Environment:
        for env in self.environment_options:
            if env.checked:
                return env.environment
        return Environment.QA
