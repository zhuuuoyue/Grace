# -*- coding: utf-8 -*-

__all__ = ['SwitchEnvironmentDialogView']

from typing import Optional, Union, Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QComboBox, QSpacerItem, QSizePolicy

from ui.utils import create_row_title, create_row_layout, create_column_layout

from extensions.glodon.environment import Environment

from .environment_button import EnvironmentButton


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
