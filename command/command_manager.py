# -*- coding: utf-8 -*-

from typing import Dict, Sequence, Optional, Union, Tuple

from .command_base import CommandBase


class CommandData(object):

    def __init__(self, command_id: str, command: CommandBase, name: Optional[str] = None):
        self.command_id: str = command_id
        self.command: CommandBase = command
        self.name: Union[str, None] = name


class CommandManager(object):

    def __init__(self):
        self.__commands: Dict[str, CommandData] = dict()

    def register_command(self, command_id: str, command: CommandBase, name: Optional[str] = None):
        if isinstance(command_id, str) and isinstance(command, CommandBase) and command_id not in self.__commands:
            self.__commands[command_id] = CommandData(command_id, command, name)

    def get_quick_commands(self) -> Sequence[Tuple[str, str]]:
        result = list()
        for key in self.__commands:
            command = self.__commands[key]
            if command.name is not None:
                result.append((command.name, command.command_id))
        return result

    def execute(self, command_id: str, *args, **kwargs):
        if command_id in self.__commands:
            self.__commands[command_id].command.exec(*args, **kwargs)
