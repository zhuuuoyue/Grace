# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QLabel, QListView, QGroupBox, QTextEdit, QHBoxLayout, QLineEdit, QSpacerItem, QSizePolicy

from ui.basic import form, create_no_focus_tool_button, add_layout_children


def create_panel_title(text: str) -> QLabel:
    label = QLabel(text)
    label.setFixedHeight(22)
    return label


def create_no_focus_line_edit() -> QLineEdit:
    edit = QLineEdit()
    edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    return edit


class EditCreationSolutionsView(object):

    def __init__(self, dialog: QDialog):
        dialog.setWindowTitle(r'Edit Creation Solutions')
        dialog.setMinimumSize(1000, 600)
        dialog.setSizeGripEnabled(True)

        self.solution_title = create_panel_title(r'Solution List')
        self.add_solution = create_no_focus_tool_button('add')
        self.delete_solution = create_no_focus_tool_button('minus')
        self.edit_solution = create_no_focus_tool_button('edit')
        self.solution_top_row = QHBoxLayout()
        self.solution_top_row.setSpacing(8)
        self.solution_top_row.setContentsMargins(0, 0, 0, 0)
        add_layout_children(
            self.solution_top_row,
            children=[self.solution_title, self.add_solution, self.delete_solution, self.edit_solution]
        )

        self.solution_list = QListView()

        self.solution_panel_layout = form.create_column_layout(
            children=[self.solution_top_row, self.solution_list]
        )
        self.solution_panel = QWidget()
        self.solution_panel.setFixedWidth(240)
        self.solution_panel.setLayout(self.solution_panel_layout)

        self.document_title = create_panel_title(r'Document List')
        self.add_document = create_no_focus_tool_button('add')
        self.delete_document = create_no_focus_tool_button('minus')
        self.edit_document = create_no_focus_tool_button('edit')
        self.document_top_row = QHBoxLayout()
        self.document_top_row.setSpacing(8)
        self.document_top_row.setContentsMargins(0, 0, 0, 0)
        add_layout_children(
            self.document_top_row,
            children=[self.document_title, self.add_document, self.delete_document, self.edit_document]
        )

        self.document_list = QListView()

        self.document_relative_path_title = form.create_row_title(r'Relative Path')
        self.document_relative_path_input = create_no_focus_line_edit()
        self.document_relative_path_row = form.create_row_layout(
            title=self.document_relative_path_title,
            widget=self.document_relative_path_input
        )

        self.document_encoding_title = form.create_row_title(r'File Encoding')
        self.document_encoding_input = create_no_focus_line_edit()
        self.document_encoding_row = form.create_row_layout(
            title=self.document_encoding_title,
            widget=self.document_encoding_input
        )

        self.document_template_name_title = form.create_row_title(r'Template')
        self.document_template_name_input = create_no_focus_line_edit()
        self.document_template_name_row = form.create_row_layout(
            title=self.document_template_name_title,
            widget=self.document_template_name_input
        )

        self.document_detail = QGroupBox()
        self.document_detail.setFixedHeight(160)
        self.document_detail.setTitle(r'Document Detail')

        self.document_detail_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.document_detail_layout = form.create_column_layout(
            children=[self.document_relative_path_row, self.document_encoding_row, self.document_template_name_row, self.document_detail_spacer]
        )
        self.document_detail_layout.setContentsMargins(8, 8, 8, 8)
        self.document_detail.setLayout(self.document_detail_layout)

        self.document_panel_layout = form.create_column_layout(
            children=[self.document_top_row, self.document_list, self.document_detail]
        )
        self.document_panel = QWidget()
        self.document_panel.setFixedWidth(320)
        self.document_panel.setLayout(self.document_panel_layout)

        self.template_title = create_panel_title(r'Template Preview')
        self.template_preview = QTextEdit()
        self.template_panel_layout = form.create_column_layout(children=[self.template_title, self.template_preview])

        self.layout = QHBoxLayout()
        self.layout.setSpacing(16)
        self.layout.setContentsMargins(8, 8, 8, 8)
        add_layout_children(
            self.layout,
            children=[self.solution_panel, self.document_panel, self.template_panel_layout]
        )
        dialog.setLayout(self.layout)
