# -*- coding: utf-8 -*-

from command import ICommand

from ui.create.EditCreationTemplatesDialog import EditCreationTemplatesDialog


class EditTemplateCommand(ICommand):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs):
        dialog = EditCreationTemplatesDialog()
        dialog.initialize()
        dialog.exec()
