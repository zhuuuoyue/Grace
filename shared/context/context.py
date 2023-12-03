# -*- coding: utf-8 -*-

__all__ = ['Context']

import os
from typing import Union

from ui import ApplicationBase, MainWindowBase, SystemTrayIconBase, QuickLauncherBase


class Context(object):

    def __init__(self, *args, **kwargs):
        self.__app: Union[ApplicationBase, None] = None
        self.__main_window: Union[MainWindowBase, None] = None
        self.__quick_launcher: Union[QuickLauncherBase, None] = None
        self.__system_tray: Union[SystemTrayIconBase, None] = None
        self.__root_directory: str = ''

        self.root_directory = kwargs.get('root_directory')
        self.app = kwargs.get('main_window')
        self.main_window = kwargs.get('main_window')

    @property
    def root_directory(self) -> str:
        return self.__root_directory

    @root_directory.setter
    def root_directory(self, value: str):
        if isinstance(value, str):
            self.__root_directory = value

    @property
    def image_directory(self) -> str:
        return os.path.join(self.root_directory, 'images')

    @property
    def data_file_path(self) -> str:
        return os.path.join(self.root_directory, 'data.db')

    @property
    def app(self) -> Union[ApplicationBase, None]:
        return self.__app

    @app.setter
    def app(self, value: ApplicationBase):
        if isinstance(value, ApplicationBase):
            self.__app = value

    @property
    def main_window(self) -> Union[MainWindowBase, None]:
        return self.__main_window

    @main_window.setter
    def main_window(self, value: MainWindowBase):
        if isinstance(value, MainWindowBase):
            self.__main_window = value

    @property
    def quick_launcher(self) -> Union[QuickLauncherBase, None]:
        return self.__quick_launcher

    @quick_launcher.setter
    def quick_launcher(self, widget: QuickLauncherBase):
        self.__quick_launcher = widget

    @property
    def system_tray(self) -> Union[SystemTrayIconBase, None]:
        return self.__system_tray

    @system_tray.setter
    def system_tray(self, widget: SystemTrayIconBase):
        self.__system_tray = widget
