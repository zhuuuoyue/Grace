# -*- coding: utf-8 -*-

import os
import sys
import json
from typing import Sequence, List

from service import context
import db
import extensions
import app


def load_menus() -> Sequence[app.MenuData]:
    result: List[app.MenuData] = list()
    with open('ui.json') as fp:
        data = json.load(fp)
        modules = data['modules']
        for module in modules:
            commands = module['commands']
            actions: List[app.ActionData] = list()
            for command in commands:
                action = app.ActionData(
                    command_id=command['command_id'],
                    title=command['title'],
                    icon=command['icon'],
                    tooltip=command['tooltip']
                )
                actions.append(action)
            menu = app.MenuData(module['title'], actions)
            result.append(menu)
    return result


if __name__ == '__main__':
    context.initialize(os.getcwd())
    ctx = context.get_context()
    db.initialize(ctx.data_file_path)
    app.initialize(ctx)
    menus = load_menus()

    application = app.Application(sys.argv)

    window = app.MainWindow(menus)
    window.show()

    ctx.app = application
    ctx.main_window = window
    extensions.initialize(ctx)

    exit_code = application.exec()

    sys.exit(exit_code)
