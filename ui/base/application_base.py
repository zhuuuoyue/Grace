# -*- coding: utf-8 -*-

__all__ = ['ApplicationBase']

from typing import Sequence

from PySide6.QtWidgets import QApplication


class ApplicationBase(QApplication):

    def __init__(self, args: Sequence[str]):
        super().__init__(args)
