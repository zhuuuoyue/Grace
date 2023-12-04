# -*- coding: utf-8 -*-
from typing import NoReturn

from shared import get_context
from command import register_command
from ui import initialize_ui_cache
from events import (ApplicationWillInit, ApplicationDidInit, MainWindowDidInit, QuickLauncherDidInit,
                    SystemTrayIconDidInit)

from .create import *
from .vcs import *
from .application import Application
from .main_window import MainWindow
from .quick_launcher import QuickLauncher
from .system_tray_icon import SystemTrayIcon


class RegisterCommands(ApplicationWillInit):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs) -> NoReturn:
        # version control system
        register_command('cmd_edit_repositories', EditRepositoriesCommand())

        # create
        register_command('cmd_edit_template', EditTemplateCommand())
        register_command('cmd_edit_creation_solutions', EditCreationSolutionsCommand())
        register_command('cmd_create_using_template', CreateUsingTemplateCommand())


class InitializeUICache(ApplicationWillInit):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs) -> NoReturn:
        initialize_ui_cache(workspace_directory=kwargs.get('root_dir'))


class RecordApplicationInstance(ApplicationDidInit):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs) -> NoReturn:
        get_context().app = kwargs.get('app_instance')


class RecordMainWindowInstance(MainWindowDidInit):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs) -> NoReturn:
        get_context().main_window = kwargs.get('main_window_instance')


class RecordQuickLauncherInstance(QuickLauncherDidInit):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs) -> NoReturn:
        get_context().quick_launcher = kwargs.get('quick_launcher_instance')


class RecordSystemTrayIconInstance(SystemTrayIconDidInit):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs) -> NoReturn:
        get_context().system_tray = kwargs.get('system_tray_icon_instance')


def initialize():
    RegisterCommands()
    InitializeUICache()
    RecordApplicationInstance()
    RecordMainWindowInstance()
    RecordQuickLauncherInstance()
    RecordSystemTrayIconInstance()
