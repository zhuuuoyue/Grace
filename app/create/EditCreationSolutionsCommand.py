# -*- coding: utf-8 -*-

from command import CommandBase

from .EditCreationSolutionsDialog import EditCreationSolutionsDialog


class EditCreationSolutionsCommand(CommandBase):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs):
        dialog = EditCreationSolutionsDialog()
        dialog.initialize()
        dialog.exec()
