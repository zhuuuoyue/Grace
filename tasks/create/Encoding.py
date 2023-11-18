# -*- coding: utf-8 -*-

from typing import Optional

from .Identifiable import Identifiable


class Encoding(Identifiable):

    def __init__(self, name: str, id_value: Optional[int] = None):
        super().__init__(id_value=id_value)
        self.name = name
