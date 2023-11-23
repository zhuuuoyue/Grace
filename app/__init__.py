# -*- coding: utf-8 -*-

from shared.context import Context
from command import register_command

from ui.cache import initialize_ui_cache

from .create import *
from .vcs import *
from .Application import Application
from .MainWindow import MainWindow, MenuData, ActionData


def _register_commands():
    # version control system
    register_command('cmd_edit_repositories', EditRepositoriesCommand())

    # create
    register_command('cmd_edit_template', EditTemplateCommand())
    register_command('cmd_edit_creation_solutions', EditCreationSolutionsCommand())


def initialize(ctx: Context):
    initialize_ui_cache(ctx.root_directory)
    _register_commands()
