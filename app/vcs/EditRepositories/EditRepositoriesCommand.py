# -*- coding: utf-8 -*-

from command import ICommand

from .EditRepositoriesDialog import EditRepositoriesDialog


class EditRepositoriesCommand(ICommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def exec(self, *args, **kwargs):
        dialog = EditRepositoriesDialog()
        dialog.exec()
