# -*- coding: utf-8 -*-

import os
import sys
import json
from typing import Sequence, List

from ui import Application, MainWindow, MenuData, ActionData, register_commands
import context
import db
import exts


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
    context.initialize(os.getcwd())
    ctx = context.get_context()
    db.initialize(ctx.data_file_path)
    menus = load_menus()
    register_commands()

    app = Application(sys.argv)

    win = MainWindow(menus)
    win.move(0, 0)
    win.show()

    ctx.app = app
    ctx.main_window = win
    exts.initialize(ctx)

    exit_code = app.exec()

    sys.exit(exit_code)
