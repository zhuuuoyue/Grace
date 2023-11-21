# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QTextEdit


class CreationTemplateViewer(QTextEdit):

    def __init__(self, text: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setStyleSheet(
            '''
            font-family: 'Consolas';
            font-size: 14px;
            '''
        )
