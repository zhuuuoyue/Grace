# -*- coding: utf-8 -*-

from sys import argv
from json import load
from typing import Sequence, List

from ui import Application, MainWindow, MenuData, ActionData


def register_commands():
    pass


def load_menus() -> Sequence[MenuData]:
    result: List[MenuData] = list()
    with open('ui.json') as fp:
        data = load(fp)
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
    menus = load_menus()
    if len(menus) != 0:
        register_commands()

        app = Application(argv)
        win = MainWindow(menus)
        win.move(0, 0)
        win.show()
        app.exec()
