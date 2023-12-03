# -*- coding: utf-8 -*-

__all__ = ['MainWindow']

from typing import Optional, Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QCloseEvent

from ui import MainWindowBase, MenuData


class MainWindow(MainWindowBase):

    def __init__(self, menus: Sequence[MenuData], parent: Optional[QWidget] = None,
                 flags: Qt.WindowType = Qt.WindowType.Window):
        super().__init__(object_name='AE4FD4EA-66E5-421A-B944-410E17E260DF', parent=parent, flags=flags,
                         window_icon='cat-eyes', window_title='Grace - Make your programming graceful')
        self.initialize(menus)

    def initialize(self, menus: Sequence[MenuData]):
        self.setFixedHeight(22)
        self.setMinimumWidth(512)
        self.add_menus(menus)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.hide()
        event.ignore()
