# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtGui import QIcon

from .utils import get_image_path


__all__ = ['Icon']


class Icon(QIcon):

    def __init__(self, icon_id: Optional[str] = None):
        if icon_id is None or len(icon_id) == 0:
            icon_path = get_image_path('cat-48')
        else:
            icon_path = get_image_path(icon_id)
        super().__init__(icon_path)
