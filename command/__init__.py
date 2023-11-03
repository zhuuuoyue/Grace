# -*- coding: utf-8 -*-

from .ICommand import ICommand
from .CommandManager import CommandManager


__command_manager: CommandManager = CommandManager()


def get_command_manager() -> CommandManager:
    return __command_manager


def register_command(command_id: str, command: ICommand):
    get_command_manager().register_command(command_id, command)


def execute_command(command_id: str, *args, **kwargs):
    get_command_manager().execute(command_id, *args, **kwargs)
