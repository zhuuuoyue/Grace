# -*- coding: utf-8 -*-

from typing import Dict

from .ICommand import ICommand


class CommandManager(object):

    def __init__(self):
        self.__commands: Dict[str, ICommand] = dict()

    def register_command(self, command_id: str, command: ICommand):
        if isinstance(command_id, str) and isinstance(command, ICommand) and command_id not in self.__commands:
            self.__commands[command_id] = command

    def execute(self, command_id: str, *args, **kwargs):
        if command_id in self.__commands:
            self.__commands[command_id].exec(*args, **kwargs)
