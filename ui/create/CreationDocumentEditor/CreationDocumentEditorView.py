# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QDialog, QLineEdit, QComboBox, QSpacerItem, QSizePolicy

from ui.basic import form, create_no_focus_button, create_no_focus_tool_button

from ui.create.CreationTemplateViewer import CreationTemplateViewer


class CreationDocumentEditorView(object):

    def __init__(self, dialog: QDialog):
        dialog.setWindowTitle(r'模板文档编辑器')
        dialog.setSizeGripEnabled(True)

        self.relative_path_title = form.create_row_title(r'相对路径')
        self.relative_path_input = QLineEdit()
        self.relative_path_layout = form.create_row_layout(title=self.relative_path_title, widget=self.relative_path_input)

        self.encoding_title = form.create_row_title(r'文件编码')
        self.encoding_selector = QComboBox()
        self.encoding_layout = form.create_row_layout(title=self.encoding_title, widget=self.encoding_selector)

        self.template_title = form.create_row_title(r'文档模板')
        self.template_selector = QComboBox()
        self.template_spacer = QSpacerItem(8, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.preview_button = create_no_focus_tool_button('cat-48')
        self.template_layout = form.create_row_layout(
            title=self.template_title,
            widgets=[self.template_selector, self.template_spacer, self.preview_button]
        )

        self.template_preview = CreationTemplateViewer()
        self.confirm_button = create_no_focus_button(r'')

        self.layout = form.create_column_layout(
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
