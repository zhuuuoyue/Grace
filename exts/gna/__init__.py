# -*- coding: utf-8 -*-

from command import register_command
from context import Context
from ui import ActionData, MainWindow

from .CleanLogFiles import CleanLogFilesCommand


def initialize(ctx: Context):
    register_command('cmd_clean_log_files', CleanLogFilesCommand())

    win = ctx.main_window
    menu = 'GNA'
    if isinstance(win, MainWindow):
        win.add_action(menu, ActionData(command_id='cmd_clean_log_files', title='Clean Log Files', icon='clean',
                                        tooltip='Clean log files under architecture and structure software package'))
