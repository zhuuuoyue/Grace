# -*- coding: utf-8 -*-


class CommandInfo(object):

    def __init__(self, name: str, command_id: str):
        self.name: str = name
        self.command_id: str = command_id

    def __eq__(self, other):
        if not isinstance(other, CommandInfo):
            return False
        return self.name == other.name and self.command_id == other.command_id

    def __lt__(self, other):
        if not isinstance(other, CommandInfo):
            return True
        return self.name < other.name
