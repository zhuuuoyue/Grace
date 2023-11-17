# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QTextEdit, QVBoxLayout


class TemplateViewerView(object):

    def __init__(self, dialog: QDialog):
        dialog.setMinimumSize(400, 300)
        dialog.resize(400, 300)
        dialog.setSizeGripEnabled(True)

        self.editor = QTextEdit()
        self.editor.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.editor.setStyleSheet(
            '''border: none;
            font-family: 'Consolas';
            font-size: 14px;'''
        )

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.editor)

        dialog.setLayout(self.layout)
