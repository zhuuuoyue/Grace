# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QSystemTrayIcon, QMenu

from ui import Icon


class SystemTrayView(object):

    def __init__(self, tray: QSystemTrayIcon):
        self.menu = QMenu(tray.parent())
        self.open_main_window_action = self.menu.addAction(Icon(), 'Open Main Window')
        self.open_quick_launcher_action = self.menu.addAction(Icon(), 'Open Quick Launcher')
        self.open_settings_action = self.menu.addAction(Icon(), 'Open Settings')
        self.separator = self.menu.addSeparator()
        self.quit_action = self.menu.addAction('Quit')
        tray.setContextMenu(self.menu)
