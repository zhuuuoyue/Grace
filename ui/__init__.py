# -*- coding: utf-8 -*-

from command import register_command
from context import Context

from .Application import Application
from .MainWindow import MainWindow, MenuData, ActionData, Action
from .vcs import *
from .basic.UICache import get_ui_cache, initialize_ui_cache


def register_commands():
    register_command('cmd_edit_repositories', EditRepositoriesCommand())


def initialize(ctx: Context):
    initialize_ui_cache(ctx.root_directory)
