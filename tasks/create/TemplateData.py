# -*- coding: utf-8 -*-

from typing import Optional


class TemplateData(object):

    def __init__(self, name: Optional[str] = None, content: Optional[str] = None):
        self.name: str = str() if name is None else name
        self.content: str = str() if content is None else content
