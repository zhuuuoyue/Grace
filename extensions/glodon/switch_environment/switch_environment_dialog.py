# -*- coding: utf-8 -*-

__all__ = ['SwitchEnvironmentDialog']

from typing import List, Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from ui import DialogBase

from extensions.glodon.environment import Environment

from .environment_option import EnvironmentOption
from .environment_button import EnvironmentButton
from .switch_environment_task import SwitchEnvironmentTask
from .switch_environment_dialog_view import SwitchEnvironmentDialogView
from .switch_environment_dialog_view_model import SwitchEnvironmentDialogViewModel


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
