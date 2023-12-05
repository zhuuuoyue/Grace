# -*- coding: utf-8 -*-

import os
import sys
from typing import NoReturn

from shared import context
import db
import extensions
import app
from events import get_event_handler_manager, ApplicationWillInit


class InitializeContext(ApplicationWillInit):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs) -> NoReturn:
        root_dir = kwargs.get('root_dir')
        context.initialize_context(root_directory=root_dir)
        context.get_context().debug_mode = os.path.isfile(os.path.join(root_dir, 'debug'))


if __name__ == '__main__':
    InitializeContext()
    app.initialize()
    db.initialize()
    extensions.initialize()

    event_handler_manager = get_event_handler_manager()

    event_handler_manager.application_will_init(root_dir=os.getcwd())
    application = app.Application(sys.argv)
    event_handler_manager.application_did_init(app_instance=application)

    event_handler_manager.main_window_will_init()
    window = app.MainWindow()
    event_handler_manager.main_window_did_init(main_window_instance=window)

    ctx = context.get_context()
    if ctx.debug_mode:
        window.show()

    event_handler_manager.extensions_will_load()
    extensions.load()
    event_handler_manager.extensions_did_load()

    event_handler_manager.quick_launcher_will_init()
    quick_launcher = app.QuickLauncher()
    event_handler_manager.quick_launcher_did_init(quick_launcher_instance=quick_launcher)

    event_handler_manager.system_tray_icon_will_init()
    system_tray_icon = app.SystemTrayIcon(window)
    event_handler_manager.system_tray_icon_did_init(system_tray_icon_instance=system_tray_icon)

    event_handler_manager.system_tray_icon_will_show()
    system_tray_icon.show()
    event_handler_manager.system_tray_icon_did_show()

    event_handler_manager.application_will_exec()
    exit_code = application.exec()
    event_handler_manager.application_did_exec()
    sys.exit(exit_code)
