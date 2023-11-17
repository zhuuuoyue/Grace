# -*- coding: utf-8 -*-

from command import ICommand

from ui.create.EditTemplatesDialog.EditTemplatesDialog import EditTemplatesDialog


class EditTemplateCommand(ICommand):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs):
        dialog = EditTemplatesDialog()
        dialog.initialize()
        dialog.exec()
