# -*- coding: utf-8 -*-

import os
import sys
import json
from typing import Sequence, List

from ui import Application, MainWindow, MenuData, ActionData, register_commands
from db import initialize


def load_menus() -> Sequence[MenuData]:
    result: List[MenuData] = list()
    with open('ui.json') as fp:
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


if __name__ == '__main__':
    initialize(f'{os.getcwd()}\\data.db')
    menus = load_menus()
    register_commands()

    app = Application(sys.argv)
    win = MainWindow(menus)
    win.move(0, 0)
    win.show()
    exit_code = app.exec()

    sys.exit(exit_code)
