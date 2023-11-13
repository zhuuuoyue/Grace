# -*- coding: utf-8 -*-

from typing import Sequence, Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QDialog, QRadioButton

from .SwitchEnvironmentDialogViewModel import SwitchEnvironmentDialogViewModel
from .SwitchEnvironmentDialogView import SwitchEnvironmentDialogView
from .SwitchEnvironmentTask import SwitchEnvironmentTask


class SwitchEnvironmentDialog(QDialog):

    def __init__(self, packages: Sequence[str], task: SwitchEnvironmentTask, parent: Optional[QWidget] = None):
        super().__init__(parent)
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
