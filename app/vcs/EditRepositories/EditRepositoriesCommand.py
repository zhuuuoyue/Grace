# -*- coding: utf-8 -*-

from command import CommandBase

from .EditRepositoriesDialog import EditRepositoriesDialog


class EditRepositoriesCommand(CommandBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def exec(self, *args, **kwargs):
        dialog = EditRepositoriesDialog()
        dialog.exec()
