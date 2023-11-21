# -*- coding: utf-8 -*-

from typing import Optional

from .Identifiable import Identifiable


class SolutionData(Identifiable):

    def __init__(self, name: Optional[str] = None, object_id: Optional[int] = None):
        super().__init__(id_value=object_id)
        self.name: str = str() if name is None else name
