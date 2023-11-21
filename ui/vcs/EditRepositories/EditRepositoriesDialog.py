# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget

from .EditRepositoriesView import EditRepositoriesView


class EditRepositoriesDialog(QDialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui = EditRepositoriesView(self)
