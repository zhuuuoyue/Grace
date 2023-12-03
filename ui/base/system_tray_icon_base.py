# -*- coding: utf-8 -*-

__all__ = ['SystemTrayIconBase']

from typing import Optional

from PySide6.QtWidgets import QSystemTrayIcon, QWidget
from PySide6.QtGui import QIcon


class SystemTrayIconBase(QSystemTrayIcon):

    def __init__(self, icon: QIcon, parent: Optional[QWidget] = None):
        super().__init__(icon=icon, parent=parent)
