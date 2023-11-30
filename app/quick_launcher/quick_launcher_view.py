# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from ui.utils import add_layout_children

from .keyword_input import KeywordInput
from .candidate_list import CandidateList


class QuickLauncherView(object):

    def __init__(self, window: QMainWindow):
        window.setFixedWidth(512)

        self.keyword_input = KeywordInput()
        self.keyword_input.setFixedHeight(40)
        self.keyword_input.setStyleSheet(
            '''
            border: 3px solid gray;
            border-radius: 5px;
            font-family: 'Microsoft YaHei';
            font-size: 24px;
            color: gray;
            '''
        )

        self.candidates = CandidateList()
        self.candidates.setStyleSheet(
            '''
            font-family: 'Microsoft YaHei';
            font-size: 18px;
            color: gray;
            border: none;
            '''
        )

        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(1, 1, 1, 1)
        add_layout_children(self.layout, children=[self.keyword_input, self.candidates])

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        window.setCentralWidget(self.central_widget)
