# -*- coding: utf-8 -*-

from command import ICommand

from ..utils import detect_software_packages

from .SwitchEnvironmentDialog import SwitchEnvironmentDialog
from .SwitchEnvironmentTask import SwitchEnvironmentTask


class SwitchEnvironmentCommand(ICommand):

    def exec(self, *args, **kwargs):
        packages = detect_software_packages()
        task = SwitchEnvironmentTask()
        dialog = SwitchEnvironmentDialog(packages, task)
        dialog.exec()
