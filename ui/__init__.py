# -*- coding: utf-8 -*-

from command import register_command
from .Application import Application
from .MainWindow import MainWindow, MenuData, ActionData, Action
from .vcs import *


def register_commands():
    register_command('cmd_edit_repositories', EditRepositoriesCommand())
