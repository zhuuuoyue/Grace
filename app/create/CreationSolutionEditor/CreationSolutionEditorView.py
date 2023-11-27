# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QDialog, QLineEdit, QVBoxLayout

from ui.utils import create_no_focus_button


class CreationSolutionEditorView(object):

    def __init__(self, dialog: QDialog):
        dialog.setFixedSize(480, 70)

        self.input = QLineEdit()
        self.confirm = create_no_focus_button('')
        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.confirm)
        dialog.setLayout(self.layout)
