# -*- coding: utf-8 -*-

from shared.context import Context
from command import register_command

from ui import initialize_ui_cache

from .create import *
from .vcs import *
from .application import Application
from .main_window import MainWindow
from .quick_launcher import QuickLauncher
from .system_tray_icon import SystemTrayIcon


def _register_commands():
    # version control system
    register_command('cmd_edit_repositories', EditRepositoriesCommand())

    # create
    register_command('cmd_edit_template', EditTemplateCommand())
    register_command('cmd_edit_creation_solutions', EditCreationSolutionsCommand())
    register_command('cmd_create_using_template', CreateUsingTemplateCommand())


def initialize(ctx: Context):
    initialize_ui_cache(ctx.root_directory)
    _register_commands()
