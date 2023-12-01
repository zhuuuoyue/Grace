# -*- coding: utf-8 -*-

from typing import Sequence

from .action_data import ActionData


class MenuData(object):

    def __init__(self, title: str, actions: Sequence[ActionData]):
        self.title: str = title
        self.actions: Sequence[ActionData] = actions
