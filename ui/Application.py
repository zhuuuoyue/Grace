# -*- coding: utf-8 -*-

from typing import Sequence

from PySide6.QtWidgets import QApplication


class Application(QApplication):

    def __init__(self, args: Sequence[str]):
        super().__init__(args)
