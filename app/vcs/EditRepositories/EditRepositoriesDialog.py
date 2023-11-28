# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtWidgets import QWidget

from .EditRepositoriesView import EditRepositoriesView

from ui.base import DialogBase


class EditRepositoriesDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(object_name='09532fc6-1734-4877-8b0b-160cd4df389a', parent=parent,
                         window_title='Edit Repositories and Branches')
        self.ui = EditRepositoriesView(self)
