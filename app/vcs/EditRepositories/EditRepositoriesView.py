# -*- coding: utf-8 -*-

from typing import Sequence

from PySide6.QtWidgets import (
    QWidget, QDialog, QLabel, QListView, QToolButton, QTreeView, QTableView,
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)

from ui import Icon


class EditRepositoriesView(object):

    def __init__(self, dialog: QDialog):
        self.initialize_repository_panel()
        self.initialize_branch_panel()
        self.initialize_detail_panel()

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.repository_layout)
        self.layout.addLayout(self.branch_layout)
        self.layout.addLayout(self.detail_layout)

        dialog.setWindowTitle(r'编辑仓库和分支信息')
        dialog.setMinimumSize(600, 400)
        dialog.resize(600, 400)
        dialog.setSizeGripEnabled(True)
        dialog.setLayout(self.layout)

    def initialize_repository_panel(self):
        self.repository_title = QLabel(r'仓库列表')
        self.repository_list = QListView()
        self.add_repository = QToolButton()
        self.add_repository.setIcon(Icon('add'))
        self.add_repository.setToolTip(r'添加仓库')
        self.remove_repository = QToolButton()
        self.remove_repository.setIcon(Icon('minus'))
        self.remove_repository.setToolTip(r'移除仓库')
        self.repository_button_layout = self.create_tool_button_bar([self.add_repository, self.remove_repository])
        self.repository_layout = self.create_panel_layout(
            self.repository_title, self.repository_list, self.repository_button_layout)

    def initialize_branch_panel(self):
        self.branch_title = QLabel(r'分支列表')
        self.branch_tree = QTreeView()
        self.add_branch = QToolButton()
        self.remove_branch = QToolButton()
        self.update_branches = QToolButton()
        self.branch_button_layout = self.create_tool_button_bar(
            [self.add_branch, self.remove_branch, self.update_branches])
        self.branch_layout = self.create_panel_layout(self.branch_title, self.branch_tree, self.branch_button_layout)

    def initialize_detail_panel(self):
        self.detail_title = QLabel(r'分支详情')
        self.detail_table = QTableView()
        self.update_detail = QToolButton()
        self.update_button_layout = self.create_tool_button_bar([self.update_detail])
        self.detail_layout = self.create_panel_layout(self.detail_title, self.detail_table, self.update_button_layout)

    @staticmethod
    def create_tool_button_bar(widgets: Sequence[QWidget]) -> QHBoxLayout:
        layout = QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addSpacerItem(spacer)
        return layout

    @staticmethod
    def create_panel_layout(title: QLabel, body: QWidget, foot: QHBoxLayout) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(body)
        layout.addLayout(foot)
        return layout
