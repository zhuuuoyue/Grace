# -*- coding: utf-8 -*-

from typing import Optional, Union


class Identifiable(object):

    def __init__(self, id_value: Optional[int] = None):
        self.__id: int = 0 if id_value is None else id_value

    def get_id(self) -> int:
        return self.__id

    id = property(fget=get_id)

    def __lt__(self, other) -> bool:
        return self.id < other.id if isinstance(other, Identifiable) else True
