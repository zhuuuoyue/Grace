# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QDialog, QWidget, QToolButton, QListView,
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)

from ui import Icon

from app.create.CreationTemplateViewer import CreationTemplateViewer

from .EditCreationTemplatesViewModel import EditCreationTemplatesViewModel


class EditCreationTemplatesView(object):

    def __init__(self, dialog: QDialog, vm: EditCreationTemplatesViewModel):
        dialog.setMinimumSize(800, 600)
        dialog.setSizeGripEnabled(True)

        self.new_button = self.create_tool_button('add-file', 'New')
        self.remove_button = self.create_tool_button('remove', 'Delete')
        self.edit_button = self.create_tool_button('edit', 'Edit')
        self.copy_button = self.create_tool_button('copy', 'Copy')
        self.export_button = self.create_tool_button('export', 'Export')
        self.import_button = self.create_tool_button('import', 'Import')
        self.tool_button_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)

        self.tool_button_layout = QHBoxLayout()
        self.tool_button_layout.setSpacing(4)
        self.tool_button_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_button_layout.addWidget(self.new_button)
        self.tool_button_layout.addWidget(self.remove_button)
        self.tool_button_layout.addWidget(self.edit_button)
        self.tool_button_layout.addWidget(self.copy_button)
        self.tool_button_layout.addWidget(self.export_button)
        self.tool_button_layout.addWidget(self.import_button)
        self.tool_button_layout.addSpacerItem(self.tool_button_spacer)

        self.template_list = QListView()

        self.left_panel_layout = QVBoxLayout()
        self.left_panel_layout.setSpacing(4)
        self.left_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.left_panel_layout.addLayout(self.tool_button_layout)
        self.left_panel_layout.addWidget(self.template_list)

        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(240)
        self.left_panel.setLayout(self.left_panel_layout)

        self.template_preview = CreationTemplateViewer()
        self.template_preview.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.addWidget(self.left_panel)
        self.layout.addWidget(self.template_preview)
        dialog.setLayout(self.layout)

        # load ata
        self.new_button.setEnabled(vm.new_button_enabled)
        self.remove_button.setEnabled(vm.remove_button_enabled)
        self.edit_button.setEnabled(vm.edit_button_enabled)
        self.copy_button.setEnabled(vm.copy_button_enabled)
        self.export_button.setEnabled(vm.export_button_enabled)
        self.import_button.setEnabled(vm.import_button_enabled)

        self.template_list.setModel(vm.template_list_model)
        self.template_list.setCurrentIndex(vm.current_template_index)

        self.template_preview.setText(vm.template_preview_text)

    @staticmethod
    def create_tool_button(icon: str, tooltip: str) -> QToolButton:
        button = QToolButton()
        button.setIcon(Icon(icon))
        button.setToolTip(tooltip)
        return button
