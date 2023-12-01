# -*- coding: utf-8 -*-

__all__ = ['MainWindow']

from typing import Optional, Sequence, Union, List

from PySide6.QtCore import Qt, QObject, Slot
from PySide6.QtWidgets import QWidget, QMenuBar, QMenu
from PySide6.QtGui import QCloseEvent

from command import execute_command
from ui import MainWindowBase, Icon

from .action_data import ActionData
from .menu_data import MenuData
from .action import Action


class MainWindow(MainWindowBase):

    def __init__(self, menus: Sequence[MenuData], parent: Optional[QWidget] = None,
                 flags: Qt.WindowType = Qt.WindowType.Window):
        super().__init__(object_name='AE4FD4EA-66E5-421A-B944-410E17E260DF', parent=parent, flags=flags,
                         window_icon='cat-eyes', window_title='Grace - Make your programming graceful')
        self.initialize(menus)

    def initialize(self, menus: Sequence[MenuData]):
        self.setFixedHeight(22)
        self.setMinimumWidth(512)

        for menu_data in menus:
            menu = self.get_menu(menu_data.title)
            if menu is None:
                continue
            for action_data in menu_data.actions:
                self.add_action(menu_data.title, action_data)

    def get_menu(self, text: str) -> Union[QMenu, None]:
        if not isinstance(text, str) or text == str():
            return None
        menu_bar: QMenuBar = self.menuBar()
        menus: List[QObject] = menu_bar.children()
        for menu in menus:
            if isinstance(menu, QMenu) and menu.title() == text:
                return menu
        menu = menu_bar.addMenu(text)
        return menu

    def add_action(self, menu: str, action_data: ActionData):
        menu = self.get_menu(menu)
        if menu is None:
            return
        action = Action(action_data.command_id, action_data.title, menu)
        action.setIcon(Icon(action_data.icon))
        action.setToolTip(action_data.tooltip)
        action.clicked.connect(self.__on_clicked)
        menu.addAction(action)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.hide()
        event.ignore()

    @Slot(str)
    def __on_clicked(self, command_id: str):
        execute_command(command_id)
