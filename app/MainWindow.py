# -*- coding: utf-8 -*-

from typing import Optional, Sequence, Union, List

from PySide6.QtCore import Qt, QObject, Signal, Slot
from PySide6.QtWidgets import QWidget, QMenuBar, QMenu
from PySide6.QtGui import QAction, QCloseEvent

from command import execute_command
from ui import MainWindowBase, Icon


class ActionData(object):

    def __init__(self, command_id: str, title: str, icon: Optional[str] = None, tooltip: Optional[str] = None):
        self.command_id: str = command_id
        self.title: str = title
        self.icon: str = icon
        self.tooltip: str = tooltip


class MenuData(object):

    def __init__(self, title: str, actions: Sequence[ActionData]):
        self.title: str = title
        self.actions: Sequence[ActionData] = actions


class Action(QAction):

    clicked: Signal = Signal(str)

    def __init__(self, command_id: str, text: str, parent: Optional[QObject] = None):
        super().__init__(text=text, parent=parent)
        self.__command_id = command_id
        self.triggered.connect(self.__on_triggered)

    @Slot()
    def __on_triggered(self):
        self.clicked.emit(self.__command_id)


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
