# -*- coding: utf-8 -*-

from typing import Union

from PySide6.QtWidgets import QApplication, QMainWindow


class Context(object):

    def __init__(self, *args, **kwargs):
        self.__app: Union[QApplication, None] = None
        self.__main_window: Union[QMainWindow, None] = None

        self.app = kwargs.get('main_window')
        self.main_window = kwargs.get('main_window')

    @property
    def app(self) -> Union[QApplication, None]:
        return self.__app

    @app.setter
    def app(self, value: QApplication):
        if isinstance(value, QApplication):
            self.__app = value

    @property
    def main_window(self) -> Union[QMainWindow, None]:
        return self.__main_window

    @main_window.setter
    def main_window(self, value: QMainWindow):
        if isinstance(value, QMainWindow):
            self.__main_window = value
