# -*- coding: utf-8 -*-

from command import ICommand

from .EditTemplateDialog import EditTemplateDialog


class EditTemplateCommand(ICommand):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs):
        dialog = EditTemplateDialog()
        dialog.initialize()
        dialog.exec()
