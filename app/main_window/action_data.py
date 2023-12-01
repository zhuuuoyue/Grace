# -*- coding: utf-8 -*-

from typing import Optional


class ActionData(object):

    def __init__(self, command_id: str, title: str, icon: Optional[str] = None, tooltip: Optional[str] = None):
        self.command_id: str = command_id
        self.title: str = title
        self.icon: str = icon
        self.tooltip: str = tooltip
