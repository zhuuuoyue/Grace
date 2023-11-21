# -*- coding: utf-8 -*-

from typing import Optional

from .Identifiable import Identifiable


class TemplateData(Identifiable):

    def __init__(self, name: Optional[str] = None, content: Optional[str] = None,
                 id_value: Optional[int] = None):
        super().__init__(id_value)
        self.name: str = str() if name is None else name
        self.content: str = str() if content is None else content
