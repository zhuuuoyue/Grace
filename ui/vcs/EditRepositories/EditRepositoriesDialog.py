# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from PySide6.QtWidgets import (
    QDialog, QWidget, QLabel, QListView, QTreeView, QTableView, QToolButton,
    QLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)


class _UI(object):

    def __init__(self, dialog: QDialog):
        self.__create_repository_panel()
        self.__create_branch_panel()
        self.__create_detail_panel()

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.repository_layout)
        self.layout.addLayout(self.branch_layout)
        self.layout.addLayout(self.detail_layout)

        dialog.setWindowTitle('Edit Repositories and Branches')
        dialog.setMinimumSize(600, 400)
        dialog.resize(600, 400)
        dialog.setSizeGripEnabled(True)
        dialog.setLayout(self.layout)

    def __create_repository_panel(self):
        self.repository_title = QLabel('Repositories')
        self.repository_list = QListView()
        self.add_repository = QToolButton()
        self.remove_repository = QToolButton()
        self.repository_button_layout = self.__create_tool_button_bar([self.add_repository, self.remove_repository])
        self.repository_layout = self.__create_panel_layout(
            self.repository_title, self.repository_list, self.repository_button_layout)

    def __create_branch_panel(self):
        self.branch_title = QLabel('Branches')
        self.branch_tree = QTreeView()
        self.add_branch = QToolButton()
        self.remove_branch = QToolButton()
        self.update_branches = QToolButton()
        self.branch_button_layout = self.__create_tool_button_bar(
            [self.add_branch, self.remove_branch, self.update_branches])
        self.branch_layout = self.__create_panel_layout(self.branch_title, self.branch_tree, self.branch_button_layout)

    def __create_detail_panel(self):
        self.detail_title = QLabel('Branch Detail')
        self.detail_table = QTableView()
        self.update_detail = QToolButton()
        self.update_button_layout = self.__create_tool_button_bar([self.update_detail])
        self.detail_layout = self.__create_panel_layout(self.detail_title, self.detail_table, self.update_button_layout)

    @staticmethod
    def __create_tool_button_bar(widgets: Sequence[QWidget]) -> QHBoxLayout:
        layout = QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addSpacerItem(spacer)
        return layout

    @staticmethod
    def __create_panel_layout(title: QLabel, body: QWidget, foot: QHBoxLayout) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(body)
        layout.addLayout(foot)
        return layout


class EditRepositoriesDialog(QDialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__ui = _UI(self)
