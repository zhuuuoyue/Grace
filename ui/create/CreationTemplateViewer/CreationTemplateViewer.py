# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtWidgets import QWidget, QDialog

from tasks.create import TemplateData

from .CreationTemplateViewerView import CreationTemplateViewerView


class CreationTemplateViewer(QDialog):

    def __init__(self, data: TemplateData, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui = CreationTemplateViewerView(self)

        self.setWindowTitle(data.name)
        self.ui.editor.setText(data.content)
