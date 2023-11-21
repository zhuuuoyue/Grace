# -*- coding: utf-8 -*-

from typing import Optional, Sequence, Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QToolButton, QLayout, QWidget, QSpacerItem, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QIcon

from .utils import get_image_path


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
