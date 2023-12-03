# -*- coding: utf-8 -*-

__all__ = ['MainWindowBase']

from typing import Optional, Sequence, Union

from PySide6.QtCore import Qt, Slot, QObject
from PySide6.QtWidgets import QMainWindow, QWidget, QMenu, QMenuBar
from PySide6.QtGui import QCloseEvent

from command import execute_command

from ui.cache import update_dialog_geometry, update_dialog_geometry_cache
from ui.components import Icon

from .action_data import ActionData
from .menu_data import MenuData
from .action import Action


class MainWindowBase(QMainWindow):

    def __init__(self,
                 object_name: Optional[str] = None,
                 parent: Optional[QWidget] = None,
                 flags: Qt.WindowType = Qt.WindowType.Window,
                 window_icon: Optional[str] = None,
                 window_title: Optional[str] = None):
        super().__init__(parent, flags)
        if isinstance(object_name, str):
            self.setObjectName(object_name)
        update_dialog_geometry(self)
        self.setWindowIcon(Icon(window_icon))
        self.setWindowTitle(str() if window_title is None else window_title)

    def get_menu(self, text: str) -> Union[QMenu, None]:
        if not isinstance(text, str) or text == str():
            return None
        menu_bar: QMenuBar = self.menuBar()
        menus: Sequence[QObject] = menu_bar.children()
        for menu in menus:
            if isinstance(menu, QMenu) and menu.title() == text:
                return menu
        menu = menu_bar.addMenu(text)
        return menu

    def add_action(self, menu_title: str, action_data: ActionData):
        menu = self.get_menu(menu_title)
        if menu is None:
            return
        action = Action(action_data.command_id, action_data.title, menu)
        action.setIcon(Icon(action_data.icon))
        action.setToolTip(action_data.tooltip)
        action.clicked.connect(self.__on_action_clicked)
        menu.addAction(action)

    def add_menu(self, menu: MenuData):
        for action in menu.actions:
            self.add_action(menu.title, action)

    def add_menus(self, menus: Sequence[MenuData]):
        for menu in menus:
            self.add_menu(menu)

    def closeEvent(self, event: QCloseEvent) -> None:
        update_dialog_geometry_cache(self, True)
        super().closeEvent(event)

    @Slot(str)
    def __on_action_clicked(self, command_id: str):
        execute_command(command_id)
