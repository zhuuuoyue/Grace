# -*- coding: utf-8 -*-

from command import register_command
from context import Context

from .Application import Application
from .MainWindow import MainWindow, MenuData, ActionData, Action
from .basic.UICache import get_ui_cache, initialize_ui_cache
from .vcs import *
from .create import *


def register_commands():
    # version control system
    register_command('cmd_edit_repositories', EditRepositoriesCommand())

    # create
    register_command('cmd_edit_template', EditTemplateCommand())
    register_command('cmd_edit_creation_solutions', EditCreationSolutionsCommand())


def initialize(ctx: Context):
    initialize_ui_cache(ctx.root_directory)
