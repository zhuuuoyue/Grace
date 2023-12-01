# -*- coding: utf-8 -*-

from command import CommandBase

from .CleanLogFilesDialog import CleanLogFilesDialog


class CleanLogFilesCommand(CommandBase):

    def __init__(self):
        pass

    def exec(self, *args, **kwargs):
        dialog = CleanLogFilesDialog()
        dialog.exec()
