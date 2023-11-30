# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QSystemTrayIcon, QWidget

from ui import Icon
from shared import get_context

from .system_tray_view import SystemTrayView


class SystemTray(QSystemTrayIcon):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(icon=Icon('pixel-cat'), parent=parent)
        self.ui = SystemTrayView(self)
        self.ui.open_main_window_action.triggered.connect(self.__on_open_main_window_clicked)
        self.ui.open_quick_launcher_action.triggered.connect(self.__on_open_quick_launcher_clicked)
        self.ui.open_settings_action.triggered.connect(self.__on_open_settings_clicked)
        self.ui.quit_action.triggered.connect(self.__on_quit_clicked)
        self.activated.connect(self.__on_activated)

    @Slot()
    def __on_open_main_window_clicked(self):
        get_context().main_window.show()

    @Slot()
    def __on_open_quick_launcher_clicked(self):
        get_context().quick_launcher.show()

    @Slot()
    def __on_open_settings_clicked(self):
        print('open settings')

    @Slot()
    def __on_quit_clicked(self):
        get_context().app.quit()

    @Slot(int)
    def __on_activated(self, reason: QSystemTrayIcon.ActivationReason):
        if QSystemTrayIcon.ActivationReason.DoubleClick == reason:
            get_context().main_window.show()
