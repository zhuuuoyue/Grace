# -*- coding: utf-8 -*-

from command import CommandBase

from app.create.EditCreationTemplatesDialog import EditCreationTemplatesDialog


class EditTemplateCommand(CommandBase):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs):
        dialog = EditCreationTemplatesDialog()
        dialog.initialize()
        dialog.exec()
