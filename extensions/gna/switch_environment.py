# -*- coding: utf-8 -*-

import os
import shutil
from copy import deepcopy
from typing import Any, List, Sequence, Optional, Union

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import (
    QWidget, QDialog, QComboBox, QLineEdit, QRadioButton, QPushButton,
    QSpacerItem, QSizePolicy
)

from command import ICommand
from ui import DialogBase
from ui.utils import create_row_title, create_row_layout, create_column_layout

from .environment import Environment, environment_to_string, infer_environment
from .utils import detect_software_packages


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
        if self.environment_options != opts:
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


class SwitchEnvironmentDialogView(object):

    def __init__(self, dialog: QDialog, vm: SwitchEnvironmentDialogViewModel):
        dialog.setWindowTitle('Switch Environment')
        dialog.setFixedHeight(160)
        dialog.setMinimumWidth(800)

        title_width = 150
        self.software_title = create_row_title('Software', width=title_width)
        self.software_selector = QComboBox()
        self.software_selector.addItems(vm.software_list)
        self.software_selector.setCurrentText(vm.selected_software)
        self.software_layout = create_row_layout(self.software_selector, self.software_title)

        self.current_environment_title = create_row_title('Current Environment', width=title_width)
        self.current_environment_input = QLineEdit()
        self.current_environment_input.setEnabled(False)
        self.current_environment_input.setText(vm.current_environment)
        self.current_environment_layout = create_row_layout(
            self.current_environment_input, self.current_environment_title)

        self.target_environment_title = create_row_title('Target Environment', width=title_width)
        self.radio_of_a = self.__create_environment_option_radio_button('A')
        self.radio_of_b = self.__create_environment_option_radio_button('B', True)
        self.radio_of_c = self.__create_environment_option_radio_button('C', True)
        self.radio_of_qa = self.__create_environment_option_radio_button('QA', True)
        self.radio_of_qa_stg = self.__create_environment_option_radio_button('QA STG', True)
        environment_option_radio_buttons = [
            self.radio_of_a, self.radio_of_b, self.radio_of_c, self.radio_of_qa, self.radio_of_qa_stg]
        self.__update_environment_options(
            environment_option_radio_buttons,
            vm.environment_options
        )
        self.target_environment_layout = create_row_layout(
            title=self.target_environment_title,
            widgets=environment_option_radio_buttons,
            append_spacer=True
        )

        self.vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.run_button = QPushButton('Run')

        self.layout = create_column_layout([
            self.software_layout,
            self.current_environment_layout,
            self.target_environment_layout,
            self.vertical_spacer,
            self.run_button
        ])
        self.layout.setContentsMargins(8, 8, 8, 8)
        dialog.setLayout(self.layout)

    @staticmethod
    def __create_environment_option_radio_button(text: str, indent: Optional[bool] = False) -> QRadioButton:
        radio = QRadioButton(text)
        if indent:
            radio.setStyleSheet('QRadioButton { margin-left: 24px; }')
        return radio

    @staticmethod
    def __update_environment_option(radio: QRadioButton, environment: EnvironmentOption):
        radio.setChecked(environment.checked)
        radio.setEnabled(environment.enabled)

    @staticmethod
    def __update_environment_options(radios: Sequence[QRadioButton], environment_options: Sequence[EnvironmentOption]):
        for radio, env_opt in zip(radios, environment_options):
            SwitchEnvironmentDialogView.__update_environment_option(radio, env_opt)

    def update_environment_options(self, env_options: Sequence[EnvironmentOption]):
        self.__update_environment_options(
            [self.radio_of_a, self.radio_of_b, self.radio_of_c, self.radio_of_qa, self.radio_of_qa_stg],
            env_options
        )


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

    def __init__(self, packages: Sequence[str], task: SwitchEnvironmentTask, parent: Optional[QWidget] = None):
        super().__init__(object_name='94edc04c-e7af-452e-b2ca-4626db52e8e2', parent=parent)
        self.vm = SwitchEnvironmentDialogViewModel(packages, self)
        self.ui = SwitchEnvironmentDialogView(self, self.vm)
        self.task = task

        self.vm.current_environment_changed.connect(self.ui.current_environment_input.setText)
        self.vm.environment_options_changed.connect(self.__on_vm_environment_options_changed)

        self.ui.software_selector.currentIndexChanged.connect(self.vm.set_selected_software_package)
        self.ui.radio_of_a.clicked.connect(self.__on_ui_environment_option_check_state_changed)
        self.ui.radio_of_b.clicked.connect(self.__on_ui_environment_option_check_state_changed)
        self.ui.radio_of_c.clicked.connect(self.__on_ui_environment_option_check_state_changed)
        self.ui.radio_of_qa.clicked.connect(self.__on_ui_environment_option_check_state_changed)
        self.ui.radio_of_qa_stg.clicked.connect(self.__on_ui_environment_option_check_state_changed)
        self.ui.run_button.clicked.connect(self.__on_ui_run_button_clicked)

    @Slot()
    def __on_vm_environment_options_changed(self):
        self.ui.update_environment_options(self.vm.environment_options)

    @Slot()
    def __on_ui_environment_option_check_state_changed(self):
        sender = self.sender()
        if isinstance(sender, QRadioButton) and sender.isChecked():
            self.vm.set_environment_option_checked(sender.text())

    @Slot()
    def __on_ui_run_button_clicked(self):
        self.task.set_software_package_directory(self.vm.selected_software)
        self.task.set_target_environment(self.vm.get_target_environment())
        self.task.run()
        self.vm.update_current_environment()


class SwitchEnvironmentCommand(ICommand):

    def exec(self, *args, **kwargs):
        packages = detect_software_packages()
        task = SwitchEnvironmentTask()
        dialog = SwitchEnvironmentDialog(packages, task)
        dialog.exec()
