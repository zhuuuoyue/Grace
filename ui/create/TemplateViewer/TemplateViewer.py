# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtWidgets import QWidget, QDialog

from tasks.create import TemplateData

from .TemplateViewerView import TemplateViewerView


class TemplateViewer(QDialog):

    def __init__(self, data: TemplateData, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui = TemplateViewerView(self)

        self.setWindowTitle(data.name)
        self.ui.editor.setText(data.content)
