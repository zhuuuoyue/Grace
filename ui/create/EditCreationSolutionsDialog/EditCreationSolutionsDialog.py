# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtWidgets import QDialog, QWidget

from .EditCreationSolutionsView import EditCreationSolutionsView


class EditCreationSolutionsDialog(QDialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__ui = EditCreationSolutionsView(self)
