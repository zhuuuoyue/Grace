# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu

from command import register_command
from context import Context
from ui import Action, MainWindow

from .RunCodeReview import RunCodeReviewCommand


def initialize(ctx: Context):
    register_command('cmd_run_code_review', RunCodeReviewCommand())

    win = ctx.main_window
    if isinstance(win, MainWindow):
        mb = win.menuBar()
        m = mb.addMenu('GNA')
        win.add_action('GNA', Action('cmd_run_code_review', 'Run Code Review Batch', m))
