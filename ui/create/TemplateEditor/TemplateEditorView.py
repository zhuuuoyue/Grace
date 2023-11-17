# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLineEdit, QPlainTextEdit

from ui.basic import form, create_no_focus_button

from .TemplateEditorViewModel import TemplateEditorViewModel


class TemplateEditorView(object):

    def __init__(self, dialog: QDialog, vm: TemplateEditorViewModel):
        dialog.setWindowTitle(r'模板编辑器')
        dialog.setMinimumSize(400, 300)
        dialog.resize(600, 400)
        dialog.setSizeGripEnabled(True)

        self.name_title = form.create_row_title(r'模板名称')
        self.name_input = QLineEdit()
        self.name_layout = form.create_row_layout(title=self.name_title, widget=self.name_input)

        css = '''font-family: 'Consolas';
        font-size: 12px;'''

        self.content_title = form.create_row_title(r'模板内容')
        self.content_input = QPlainTextEdit()
        self.content_input.setStyleSheet(css)
        self.content_layout = form.create_row_layout(title=self.content_title, widget=self.content_input)
        self.content_layout.setAlignment(self.content_title, Qt.AlignmentFlag.AlignTop)

        self.parameter_title = form.create_row_title(r'参数列表')
        self.parameter_input = QPlainTextEdit()
        self.parameter_input.setFixedHeight(64)
        self.parameter_input.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.parameter_input.setStyleSheet(css)
        self.parameter_layout = form.create_row_layout(title=self.parameter_title, widget=self.parameter_input)
        self.parameter_layout.setAlignment(self.parameter_title, Qt.AlignmentFlag.AlignTop)

        self.confirm_button = create_no_focus_button(r'')

        self.layout = form.create_column_layout(
            [self.name_layout, self.content_layout, self.parameter_layout, self.confirm_button],
            spacing=8
        )
        self.layout.setContentsMargins(8, 8, 8, 8)
        dialog.setLayout(self.layout)

        # load data
        self.name_input.setText(vm.name_text)
        self.content_input.setPlainText(vm.content_text)
        self.parameter_input.setPlainText(vm.parameters_text)
        self.confirm_button.setEnabled(vm.confirm_enabled)
        self.confirm_button.setText(vm.confirm_text)
        self.confirm_button.setStyleSheet(vm.confirm_css)
