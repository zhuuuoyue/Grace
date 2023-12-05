# -*- coding: utf-8 -*-

__all__ = ['MainWindow']

import os
from typing import Optional, Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QCloseEvent

from ui import MainWindowBase, MenuData, load_menus
from shared import get_context


class MainWindow(MainWindowBase):

    def __init__(self, parent: Optional[QWidget] = None, flags: Qt.WindowType = Qt.WindowType.Window):
        super().__init__(object_name='AE4FD4EA-66E5-421A-B944-410E17E260DF', parent=parent, flags=flags,
                         window_icon='cat-eyes', window_title='Grace - Make your programming graceful')
        ui_config_filename = os.path.join(get_context().root_directory, 'ui.json')
        menus = load_menus(ui_config_filename)
        self.initialize(menus)

    def initialize(self, menus: Sequence[MenuData]):
        self.setFixedHeight(22)
        self.setMinimumWidth(512)
        self.add_menus(menus)

    def closeEvent(self, event: QCloseEvent) -> None:
        if get_context().debug_mode:
            super().closeEvent(event)
            get_context().app.quit()
        else:
            self.hide()
            event.ignore()
