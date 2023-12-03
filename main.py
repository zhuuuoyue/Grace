# -*- coding: utf-8 -*-

import os
import sys

from shared import context
import db
import extensions
import app
import ui


if __name__ == '__main__':
    application = app.Application(sys.argv)
    application.setQuitOnLastWindowClosed(False)

    context.initialize_context(os.getcwd())
    ctx = context.get_context()
    ctx.app = application
    db.initialize(ctx.data_file_path)
    app.initialize(ctx)
    menus = ui.load_menus(os.path.join(ctx.root_directory, 'ui.json'))

    window = app.MainWindow(menus)
    ctx.main_window = window
    extensions.initialize(ctx)

    quick_launcher = app.QuickLauncher()
    ctx.quick_launcher = quick_launcher

    system_tray = app.SystemTrayIcon(window)
    ctx.system_tray = system_tray
    system_tray.show()

    exit_code = application.exec()
    sys.exit(exit_code)
