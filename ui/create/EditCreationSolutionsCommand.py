# -*- coding: utf-8 -*-

from command import ICommand

from .EditCreationSolutionsDialog import EditCreationSolutionsDialog


class EditCreationSolutionsCommand(ICommand):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs):
        dialog = EditCreationSolutionsDialog()
        dialog.exec()
