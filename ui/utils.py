# -*- coding: utf-8 -*-

import os
from typing import Optional, Union, Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QToolButton,
    QLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QIcon

from shared import context


def get_image_path(image_name: str) -> str:
    return os.path.join(context.get_context().image_directory, f'{image_name}.png')


def create_no_focus_button(text: str) -> QPushButton:
    button = QPushButton(text)
    button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    return button


def create_no_focus_tool_button(icon: str, tooltip: Optional[str] = None) -> QToolButton:
    button = QToolButton()
    button.setIcon(QIcon(get_image_path(icon)))
    if tooltip is not None:
        button.setToolTip(tooltip)
    return button


def add_layout_children(layout: Union[QHBoxLayout, QVBoxLayout], children: Sequence[Union[QWidget, QSpacerItem, QLayout]]):
    for item in children:
        if isinstance(item, QWidget):
            layout.addWidget(item)
        elif isinstance(item, QSpacerItem):
            layout.addSpacerItem(item)
        elif isinstance(item, QLayout):
            layout.addLayout(item)


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
        widget: Optional[Union[QWidget, QLayout]] = None,
        title: Optional[QLabel] = None,
        title_width: Optional[int] = 80,
        append_spacer: Optional[bool] = False,
        spacing: Optional[int] = 0,
        widgets: Optional[Sequence[Union[QWidget, QLayout, QSpacerItem]]] = None
) -> QHBoxLayout:
    layout = QHBoxLayout()
    layout.setSpacing(spacing)
    if title is None:
        layout.setContentsMargins(title_width, 0, 0, 0)
    else:
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(title)
    if widget is not None:
        if isinstance(widget, QWidget):
            layout.addWidget(widget)
        elif isinstance(widget, QLayout):
            layout.addLayout(widget)
    elif widgets is not None:
        for child_widget in widgets:
            if isinstance(child_widget, QWidget):
                layout.addWidget(child_widget)
            elif isinstance(child_widget, QLayout):
                layout.addLayout(child_widget)
            elif isinstance(child_widget, QSpacerItem):
                layout.addSpacerItem(child_widget)
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
