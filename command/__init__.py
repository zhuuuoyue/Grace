# -*- coding: utf-8 -*-

from typing import Optional, Sequence, Tuple

from .command_base import CommandBase
from .command_manager import CommandManager


__command_manager: CommandManager = CommandManager()


def get_command_manager() -> CommandManager:
    return __command_manager


def register_command(command_id: str, command: CommandBase, name: Optional[str] = None):
    get_command_manager().register_command(command_id, command, name)


def execute_command(command_id: str, *args, **kwargs):
    get_command_manager().execute(command_id, *args, **kwargs)


def get_quick_commands() -> Sequence[Tuple[str, str]]:
    return get_command_manager().get_quick_commands()
