# -*- coding: utf-8 -*-

from command import ICommand

from .CleanLogFilesDialog import CleanLogFilesDialog


class CleanLogFilesCommand(ICommand):

    def __init__(self):
        pass

    def exec(self, *args, **kwargs):
        dialog = CleanLogFilesDialog()
        dialog.exec()
