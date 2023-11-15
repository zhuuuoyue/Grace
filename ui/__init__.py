# -*- coding: utf-8 -*-

from command import register_command
from .Application import Application
from .MainWindow import MainWindow, MenuData, ActionData, Action
from .vcs import *
from .create import *


def register_commands():
    # version control system
    register_command('cmd_edit_repositories', EditRepositoriesCommand())

    # create
    register_command('cmd_edit_template', EditTemplateCommand())
