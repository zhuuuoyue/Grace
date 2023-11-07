# -*- coding: utf-8 -*-

from command import register_command
from context import Context
from ui import Action, MainWindow

from .CleanLogFiles import CleanLogFilesCommand


def initialize(ctx: Context):
    register_command('cmd_clean_log_files', CleanLogFilesCommand())

    win = ctx.main_window
    if isinstance(win, MainWindow):
        mb = win.menuBar()
        m = mb.addMenu('GNA')
        win.add_action('GNA', Action('cmd_clean_log_files', 'Clean Log Files', m))
