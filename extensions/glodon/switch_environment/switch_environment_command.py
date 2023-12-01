# -*- coding: utf-8 -*-

__all__ = ['SwitchEnvironmentCommand']

from command import CommandBase

from .switch_environment_task import SwitchEnvironmentTask
from .switch_environment_dialog import SwitchEnvironmentDialog


class SwitchEnvironmentCommand(CommandBase):

    def exec(self, *args, **kwargs):
        task = SwitchEnvironmentTask()
        dialog = SwitchEnvironmentDialog(task)
        dialog.initialize()
        dialog.exec()
