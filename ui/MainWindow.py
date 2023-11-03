# -*- coding: utf-8 -*-

from typing import Optional, Sequence

from PySide6.QtCore import Qt, QObject, Signal, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QMenuBar, QMenu
from PySide6.QtGui import QAction

from command import execute_command


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


class MainWindow(QMainWindow):

    def __init__(self, menus: Sequence[MenuData], parent: Optional[QWidget] = None,
                 flags: Qt.WindowType = Qt.WindowType.Window):
        super().__init__(parent, flags)
        self.initialize(menus)

    def initialize(self, menus: Sequence[MenuData]):
        self.setWindowTitle('Grace - Make your programming graceful')
        self.setFixedHeight(22)
        self.setMinimumWidth(512)

        menu_bar: QMenuBar = self.menuBar()
        for menu_data in menus:
            menu: QMenu = menu_bar.addMenu(menu_data.title)
            for action_data in menu_data.actions:
                action = Action(action_data.command_id, action_data.title, menu)
                action.clicked.connect(self.__on_clicked)
                menu.addAction(action)

    @Slot(str)
    def __on_clicked(self, command_id: str):
        execute_command(command_id)
