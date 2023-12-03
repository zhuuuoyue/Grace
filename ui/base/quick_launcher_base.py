# -*- coding: utf-8 -*-

__all__ = ['QuickLauncherBase']

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget


class QuickLauncherBase(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent, flags=(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint))
