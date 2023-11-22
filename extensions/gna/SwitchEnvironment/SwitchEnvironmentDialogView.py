# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from PySide6.QtWidgets import QDialog, QComboBox, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QRadioButton

from ui.utils import create_row_title, create_row_layout, create_column_layout

from .SwitchEnvironmentDialogViewModel import SwitchEnvironmentDialogViewModel, EnvironmentOption


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
