# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Qt, Slot, QModelIndex
from PySide6.QtWidgets import QWidget, QMainWindow

from command import execute_command

from .quick_launcher_view import QuickLauncherView
from .quick_launcher_view_model import QuickLauncherViewModel


class QuickLauncher(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent, flags=Qt.WindowType.FramelessWindowHint)
        self.ui = QuickLauncherView(self)
        self.vm = QuickLauncherViewModel(self)
        self.initialize()

    def initialize(self):
        self.ui.keyword_input.textChanged.connect(self.__on_ui_keyword_changed)
        self.ui.keyword_input.key_up_pressed.connect(self.__on_ui_key_previous_pressed)
        self.ui.keyword_input.key_down_pressed.connect(self.__on_ui_key_next_pressed)
        self.ui.keyword_input.key_enter_pressed.connect(self.__on_ui_key_enter_pressed)
        self.ui.keyword_input.key_escape_pressed.connect(self.__on_ui_key_escape_pressed)
        self.ui.keyword_input.focus_lost.connect(self.__on_ui_focus_lost)
        self.ui.candidates.clicked.connect(self.__on_ui_candidate_clicked)
        self.ui.candidates.focus_lost.connect(self.__on_ui_focus_lost)
        self.ui.candidates.setModel(self.vm.candidate_model)

        self.vm.current_command_index_changed.connect(self.__on_vm_current_command_index_changed)
        self.vm.initialize()

    def execute_current_command(self):
        command_id = self.vm.get_current_command()
        if command_id is not None:
            execute_command(command_id)

    def show_me(self):
        self.vm.update_keyword('')
        self.show()

    def hide_me(self):
        self.hide()

    @Slot(str)
    def __on_ui_keyword_changed(self, text: str):
        keyword = text.strip()
        self.vm.update_keyword(keyword)

    @Slot()
    def __on_ui_key_next_pressed(self):
        self.vm.switch_to_next_command_option()

    @Slot()
    def __on_ui_key_previous_pressed(self):
        self.vm.switch_to_previous_command_option()

    @Slot()
    def __on_ui_key_enter_pressed(self):
        self.hide_me()
        self.execute_current_command()

    @Slot()
    def __on_ui_key_escape_pressed(self):
        self.hide_me()

    @Slot(QModelIndex)
    def __on_ui_candidate_clicked(self, current_index: QModelIndex):
        self.vm.set_current_command_index(current_index)
        self.hide_me()
        self.execute_current_command()

    @Slot()
    def __on_ui_focus_lost(self):
        self.hide_me()

    @Slot(QModelIndex)
    def __on_vm_current_command_index_changed(self, current_command_index: QModelIndex):
        self.ui.candidates.setCurrentIndex(current_command_index)
