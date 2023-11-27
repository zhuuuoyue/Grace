# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QDialog, QLineEdit, QComboBox, QSpacerItem, QSizePolicy

from ui.utils import (
    create_no_focus_button, create_no_focus_tool_button,
    create_row_title, create_row_layout, create_column_layout
)

from app.create.CreationTemplateViewer import CreationTemplateViewer


class CreationDocumentEditorView(object):

    def __init__(self, dialog: QDialog):
        dialog.setSizeGripEnabled(True)

        self.relative_path_title = create_row_title(r'相对路径')
        self.relative_path_input = QLineEdit()
        self.relative_path_layout = create_row_layout(title=self.relative_path_title, widget=self.relative_path_input)

        self.encoding_title = create_row_title(r'文件编码')
        self.encoding_selector = QComboBox()
        self.encoding_layout = create_row_layout(title=self.encoding_title, widget=self.encoding_selector)

        self.template_title = create_row_title(r'文档模板')
        self.template_selector = QComboBox()
        self.template_spacer = QSpacerItem(8, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.preview_button = create_no_focus_tool_button('')
        self.template_layout = create_row_layout(
            title=self.template_title,
            widgets=[self.template_selector, self.template_spacer, self.preview_button]
        )

        self.template_preview = CreationTemplateViewer()
        self.confirm_button = create_no_focus_button(r'')

        self.layout = create_column_layout(
            children=[
                self.relative_path_layout,
                self.encoding_layout,
                self.template_layout,
                self.template_preview,
                self.confirm_button
            ],
            spacing=8
        )
        self.layout.setContentsMargins(8, 8, 8, 8)
        dialog.setLayout(self.layout)
