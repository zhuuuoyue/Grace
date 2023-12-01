# -*- coding: utf-8 -*-

__all__ = ['SwitchEnvironmentDialogModel']

from typing import List, Union, Optional

from PySide6.QtCore import QObject, Signal, Slot, Property

from ui import WidgetModelBase

from extensions.glodon.environment import Environment, infer_environment
from extensions.glodon.utils import detect_software_packages


class SwitchEnvironmentDialogModel(WidgetModelBase):

    software_path_list_changed = Signal(type(List[str]))
    current_software_path_changed = Signal(type(Union[str, None]))
    current_environment_changed = Signal(type(Union[Environment, None]))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__software_path_list: List[str] = list()
        self.__current_software_path: Union[str, None] = None
        self.__current_environment: Union[Environment, None] = None

    def get_software_path_list(self) -> List[str]:
        return self.__software_path_list

    def set_software_path_list(self, value: List[str]):
        if self.software_path_list != value:
            self.__software_path_list = value
            self.software_path_list_changed.emit(self.software_path_list)

    def reset_software_path_list(self):
        self.software_path_list = list()

    software_path_list = Property(
        type(List[str]),
        fget=get_software_path_list,
        fset=set_software_path_list,
        freset=reset_software_path_list,
        notify=software_path_list_changed
    )

    def get_current_software_path(self) -> Union[str, None]:
        return self.__current_software_path

    def set_current_software_path(self, value: Union[str, None]):
        if self.current_software_path != value:
            self.__current_software_path = value
            self.current_software_path_changed.emit(self.current_software_path)

    def reset_current_software_path(self):
        self.current_software_path = None if len(self.software_path_list) == 0 else self.software_path_list[0]

    current_software_path = Property(
        type(Union[str, None]),
        fget=get_current_software_path,
        fset=set_current_software_path,
        freset=reset_current_software_path,
        notify=current_software_path_changed
    )

    def get_current_environment(self) -> Union[Environment, None]:
        return self.__current_environment

    def set_current_environment(self, value: Union[Environment, None]):
        if self.current_environment != value:
            self.__current_environment = value
            self.current_environment_changed.emit(self.current_environment)

    def reset_current_environment(self):
        self.current_environment = None if self.current_software_path is None\
            else infer_environment(self.current_software_path)

    current_environment = Property(
        type(Union[Environment, None]),
        fget=get_current_environment,
        fset=set_current_environment,
        freset=reset_current_environment,
        notify=current_environment_changed
    )

    def initialize(self):
        self.software_path_list_changed.connect(self.__on_software_path_list_changed)
        self.current_software_path_changed.connect(self.__on_current_software_path_changed)
        self.update()

    def update(self):
        self.software_path_list = detect_software_packages(
            include_architecture_software_package=True,
            include_structure_software_package=True
        )

    def update_current_software_environment(self):
        self.reset_current_environment()

    @Slot(type(List[str]))
    def __on_software_path_list_changed(self, software_path_list: List[str]):
        self.reset_current_software_path()

    @Slot(type(Union[str, None]))
    def __on_current_software_path_changed(self, current_software_path: Union[str, None]):
        self.reset_current_environment()
