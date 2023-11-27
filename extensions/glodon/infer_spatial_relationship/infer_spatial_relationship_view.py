# -*- coding: utf-8 -*-

from typing import Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLineEdit, QLabel, QSpacerItem, QSizePolicy

from ui.utils import create_row_title, create_row_layout, create_column_layout

from .double_input import DoubleInput
from .line_segment_input import LineSegmentInput
from .line_segment_visualizer import LineSegmentVisualizer


class InferSpatialRelationshipView(object):

    def __init__(self, dialog: QDialog):
        dialog.setWindowTitle(r'Infer Spatial Relationship')
        dialog.setFixedSize(616, 760)

        self.visualizer = LineSegmentVisualizer()
        self.visualizer.setFixedSize(600, 600)

        self.first_line_segment_title = self.create_row_title(r'Line Segment #1')
        self.first_line_segment_input = LineSegmentInput()
        self.first_line_segment_layout = create_row_layout(
            title=self.first_line_segment_title,
            widget=self.first_line_segment_input
        )

        self.second_line_segment_title = self.create_row_title(r'Line Segment #2')
        self.second_line_segment_input = LineSegmentInput()
        self.second_line_segment_layout = create_row_layout(
            title=self.second_line_segment_title,
            widget=self.second_line_segment_input
        )

        self.angle_title = self.create_row_title(r'Angle')
        self.angle = QLineEdit()
        self.angle.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.angle.setStyleSheet(
            '''
            font-family: 'Consolas';
            font-size: 13px;
            '''
        )
        self.angle_layout = create_row_layout(title=self.angle_title, widget=self.angle)

        self.tolerance_title = self.create_row_title(r'Tolerance')
        self.degree_input, self.degree_unit = self.create_tolerance_input('degree(s)')
        self.tolerance_spacer = QSpacerItem(24, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.radian_input, self.radian_unit = self.create_tolerance_input('radian(s)')
        self.tolerance_layout = create_row_layout(
            title=self.tolerance_title,
            widgets=[self.degree_input, self.degree_unit, self.tolerance_spacer, self.radian_input, self.radian_unit],
            append_spacer=True
        )

        self.conclusion_title = self.create_row_title(r'Conclusion')
        self.conclusion = QLineEdit()
        self.conclusion.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.conclusion_layout = create_row_layout(title=self.conclusion_title, widget=self.conclusion)

        self.layout = create_column_layout(
            children=[
                self.visualizer,
                self.first_line_segment_layout,
                self.second_line_segment_layout,
                self.angle_layout,
                self.tolerance_layout,
                self.conclusion_layout
            ]
        )
        self.layout.setContentsMargins(8, 8, 8, 8)
        dialog.setLayout(self.layout)

    @staticmethod
    def create_row_title(text: str) -> QLabel:
        return create_row_title(text, width=100)

    @staticmethod
    def create_tolerance_input(unit: str) -> Tuple[DoubleInput, QLabel]:
        value_input = DoubleInput()
        value_input.setFixedWidth(96)
        value_input.setStyleSheet(
            '''
            font-family: 'Consolas';
            font-size: 13px;
            '''
        )
        unit_label = QLabel(unit)
        unit_label.setFixedWidth(80)
        unit_label.setStyleSheet(
            '''
            margin-left: 4px;
            font-family: 'Consolas';
            font-size: 13px;
            '''
        )
        return value_input, unit_label
