# -*- coding: utf-8 -*-

__all__ = ['CleanLogFilesCommand']

from command import CommandBase

from .clean_log_files_dialog import CleanLogFilesDialog


class CleanLogFilesCommand(CommandBase):

    def __init__(self):
        pass

    def exec(self, *args, **kwargs):
        dialog = CleanLogFilesDialog()
        dialog.exec()
