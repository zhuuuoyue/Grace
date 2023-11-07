# -*- coding: utf-8 -*-

from typing import Optional, Union, Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy


def create_row_title(text: str, width: Optional[int] = None, height: Optional[int] = None) -> QLabel:
    label = QLabel()
    label.setText(text)
    if isinstance(width, int):
        label.setFixedWidth(width)
    else:
        label.setFixedWidth(80)
    if isinstance(height, int):
        label.setFixedHeight(height)
    else:
        label.setFixedHeight(20)
    return label


def create_row_layout(
        widget: Union[QWidget, QLayout],
        title: Optional[QLabel] = None,
        title_width: Optional[int] = 80,
        append_spacer: Optional[bool] = False,
        spacing: Optional[int] = 0
) -> QHBoxLayout:
    layout = QHBoxLayout()
    layout.setSpacing(spacing)
    if title is None:
        layout.setContentsMargins(title_width, 0, 0, 0)
    else:
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(title)
    if isinstance(widget, QWidget):
        layout.addWidget(widget)
    elif isinstance(widget, QLayout):
        layout.addLayout(widget)
    if append_spacer:
        layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
    return layout


def create_column_layout(
        children: Sequence[Union[QWidget, QLayout, QSpacerItem]],
        append_spacer: Optional[bool] = False,
        spacing: Optional[int] = 8
) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(spacing)
    for child in children:
        if isinstance(child, QWidget):
            layout.addWidget(child)
        elif isinstance(child, QLayout):
            layout.addLayout(child)
        elif isinstance(child, QSpacerItem):
            layout.addSpacerItem(child)
    if append_spacer:
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(spacer)
    return layout
