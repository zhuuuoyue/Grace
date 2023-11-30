# -*- coding: utf-8 -*-

from typing import Tuple, Optional, List

from system_hotkey import SystemHotkey
from PySide6.QtCore import QObject, Signal


class GlobalHotKey(QObject):

    triggered = Signal(type(Tuple))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__shk = SystemHotkey()
        self.__registered_hotkeys: List[Tuple] = list()

    def __del__(self):
        for action in self.__registered_hotkeys:
            self.__shk.unregister(action)

    def emit_signal(self, action: Tuple):
        self.triggered.emit(action)

    def register(self, action: Tuple):
        self.__shk.register(action, callback=lambda x: self.emit_signal(action))
        self.__registered_hotkeys.append(action)
