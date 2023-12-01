# -*- coding: utf-8 -*-

__all__ = ['DialogGeometry']

from PySide6.QtCore import QPoint, QSize


class DialogGeometry(object):

    def __init__(self, position: QPoint, size: QSize):
        self.position: QPoint = position
        self.size: QSize = size
