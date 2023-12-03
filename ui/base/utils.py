# -*- coding: utf-8 -*-

__all__ = ['load_menus']

import os
import json
from typing import Sequence, List

from .action_data import ActionData
from .menu_data import MenuData


def load_menus(ui_config_path: str) -> Sequence[MenuData]:
    result: List[MenuData] = list()
    if not os.path.isfile(ui_config_path):
        return result
    with open(ui_config_path, 'r') as fp:
        data = json.load(fp)
        modules = data['modules']
        for module in modules:
            commands = module['commands']
            actions: List[ActionData] = list()
            for command in commands:
                action = ActionData(
                    command_id=command['command_id'],
                    title=command['title'],
                    icon=command['icon'],
                    tooltip=command['tooltip']
                )
                actions.append(action)
            menu = MenuData(module['title'], actions)
            result.append(menu)
    return result
