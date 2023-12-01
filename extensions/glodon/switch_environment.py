# -*- coding: utf-8 -*-

import os
import shutil
from typing import Any, List, Optional, Union, Tuple

from PySide6.QtCore import QObject, Signal, Slot, Property, Qt
from PySide6.QtWidgets import QWidget, QDialog, QComboBox, QPushButton, QSpacerItem, QSizePolicy

from command import CommandBase
from ui import DialogBase, WidgetViewModelBase, WidgetModelBase, Icon
from ui.utils import create_row_title, create_row_layout, create_column_layout

from .environment import Environment, infer_environment
from .utils import detect_software_packages


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


class EnvironmentOption(object):

    def __init__(self, env: Environment, name: str, enabled: bool):
        self.environment: Environment = env
        self.name: str = name
        self.enabled: bool = enabled

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EnvironmentOption):
            return False
        return self.environment == other.environment and self.name == other.name and self.enabled == other.enabled


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


class EnvironmentButton(QPushButton):

    request_switching_environment = Signal(Environment)

    def __init__(self, environment: Environment, name: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setText(name)
        self.__environment = environment
        self.clicked.connect(self.__on_clicked)

    @Slot()
    def __on_clicked(self):
        self.request_switching_environment.emit(self.__environment)


class SwitchEnvironmentDialogView(object):

    def __init__(self, dialog: QDialog):
        dialog.setFixedHeight(68)
        dialog.setMinimumWidth(800)

        title_width = 150
        self.software_title = create_row_title('Software Package', width=title_width)
        self.software_selector = QComboBox()
        self.software_layout = create_row_layout(self.software_selector, self.software_title)

        self.target_environment_title = create_row_title('Expected Environment', width=title_width)
        self.button_a = self.create_environment_button(Environment.A, 'A')
        self.button_b, self.spacer_b = self.create_environment_button(Environment.B, 'B', True)
        self.button_c, self.spacer_c = self.create_environment_button(Environment.C, 'C', True)
        self.button_qa, self.spacer_qa = self.create_environment_button(Environment.QA, 'QA', True)
        self.button_qa_stg, self.spacer_qa_stg = self.create_environment_button(Environment.QA_STG, 'QA STG', True)
        self.target_environment_layout = create_row_layout(
            title=self.target_environment_title,
            widgets=[
                self.button_a,
                self.spacer_b, self.button_b,
                self.spacer_c, self.button_c,
                self.spacer_qa, self.button_qa,
                self.spacer_qa_stg, self.button_qa_stg
            ],
            append_spacer=True
        )

        self.layout = create_column_layout([
            self.software_layout,
            self.target_environment_layout
        ])
        self.layout.setContentsMargins(8, 8, 8, 8)
        dialog.setLayout(self.layout)

    @staticmethod
    def create_environment_button(environment: Environment, text: str, indent: Optional[bool] = False)\
            -> Union[EnvironmentButton, Tuple[EnvironmentButton, QSpacerItem]]:
        button = EnvironmentButton(environment, text)
        button.setFixedWidth(96)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        if indent:
            spacer = QSpacerItem(8, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            return button, spacer
        else:
            return button


class SwitchEnvironmentTask(object):

    def __init__(self):
        self.__path_to_software_package: Union[str, None] = None
        self.__target_environment: Environment = Environment.QA

    def set_software_package_directory(self, path_to_software_package: str):
        self.__path_to_software_package = path_to_software_package

    def set_target_environment(self, env: Environment):
        self.__target_environment = env

    def run(self):
        dst_dir = self.__path_to_software_package
        mapping = {
            Environment.A: 'a',
            Environment.B: 'b',
            Environment.C: 'c',
            Environment.QA: 'qa',
            Environment.QA_STG: 'qastg'
        }
        src_dir = os.path.join(dst_dir, 'SwitchEnvironment', mapping[self.__target_environment])
        children = os.listdir(src_dir)
        for child in children:
            full_path = os.path.join(src_dir, child)
            if os.path.isdir(full_path):
                self.replace_directory(src_dir, dst_dir, full_path)
            elif os.path.isfile(full_path):
                self.replace_file(src_dir, dst_dir, full_path)

    @staticmethod
    def replace_directory(src_dir: str, dst_dir: str, dir_path: str):
        src_dir_path = dir_path
        dst_dir_path = os.path.join(dst_dir, os.path.relpath(dir_path, src_dir))
        if not os.path.isdir(dst_dir_path):
            os.mkdir(dst_dir_path)
        to_copy_list = os.listdir(src_dir_path)
        for to_copy_item in to_copy_list:
            full_path = os.path.join(src_dir_path, to_copy_item)
            if os.path.isdir(full_path):
                SwitchEnvironmentTask.replace_directory(src_dir, dst_dir, full_path)
            elif os.path.isfile(full_path):
                SwitchEnvironmentTask.replace_file(src_dir, dst_dir, full_path)

    @staticmethod
    def replace_file(src_dir: str, dst_dir: str, file_path: str):
        src_file_path = file_path
        if not os.path.isfile(src_file_path):
            return

        dst_file_path = os.path.join(dst_dir, os.path.relpath(file_path, src_dir))
        if os.path.isfile(dst_file_path):
            os.remove(dst_file_path)
        shutil.copyfile(src_file_path, dst_file_path)


class SwitchEnvironmentDialog(DialogBase):

    def __init__(self, task: SwitchEnvironmentTask, parent: Optional[QWidget] = None):
        super().__init__(object_name='94edc04c-e7af-452e-b2ca-4626db52e8e2', parent=parent,
                         window_title='Switch Environment')
        self.vm = SwitchEnvironmentDialogViewModel(self)
        self.ui = SwitchEnvironmentDialogView(self)
        self.task = task

    def initialize(self):
        # signals from view model
        self.vm.software_path_list_changed.connect(self.__on_vm_software_path_list_changed)
        self.vm.current_software_path_index_changed.connect(self.__on_vm_current_software_path_index_changed)
        self.vm.environment_options_changed.connect(self.__on_vm_environment_options_changed)
        # signals from ui
        self.ui.software_selector.currentIndexChanged.connect(self.__on_ui_current_environment_index_changed)
        self.ui.button_a.request_switching_environment.connect(self.__on_ui_environment_button_clicked)
        self.ui.button_b.request_switching_environment.connect(self.__on_ui_environment_button_clicked)
        self.ui.button_c.request_switching_environment.connect(self.__on_ui_environment_button_clicked)
        self.ui.button_qa.request_switching_environment.connect(self.__on_ui_environment_button_clicked)
        self.ui.button_qa_stg.request_switching_environment.connect(self.__on_ui_environment_button_clicked)
        # initialize members
        self.vm.initialize()

    @Slot(type(List[str]))
    def __on_vm_software_path_list_changed(self, software_path_list: List[str]):
        self.ui.software_selector.clear()
        self.ui.software_selector.addItems(software_path_list)

    @Slot(int)
    def __on_vm_current_software_path_index_changed(self, current_software_index: int):
        self.ui.software_selector.setCurrentIndex(current_software_index)

    @Slot(type(List[EnvironmentOption]))
    def __on_vm_environment_options_changed(self, environment_options: List[EnvironmentOption]):
        buttons: List[EnvironmentButton] = [
            self.ui.button_a, self.ui.button_b, self.ui.button_c, self.ui.button_qa, self.ui.button_qa_stg
        ]
        for index in range(len(buttons)):
            environment_option = environment_options[index]
            environment_button = buttons[index]
            environment_button.setText(environment_option.name)
            environment_button.setEnabled(environment_option.enabled)

    @Slot(int)
    def __on_ui_current_environment_index_changed(self, current_environment_index: int):
        self.vm.request_switching_current_software(current_environment_index)

    @Slot(Environment)
    def __on_ui_environment_button_clicked(self, expected_environment: Environment):
        current_software_path = self.vm.model.current_software_path
        if current_software_path is not None:
            self.task.set_software_package_directory(self.vm.model.current_software_path)
            self.task.set_target_environment(expected_environment)
            self.task.run()
            self.vm.request_updating_environment_options()


class SwitchEnvironmentCommand(CommandBase):

    def exec(self, *args, **kwargs):
        task = SwitchEnvironmentTask()
        dialog = SwitchEnvironmentDialog(task)
        dialog.initialize()
        dialog.exec()
