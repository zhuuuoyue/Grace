# -*- coding: utf-8 -*-

__all__ = ['SearcherType']

from enum import IntEnum, auto


class SearcherType(IntEnum):

    LOCAL_SEARCHER = auto()
    SEARCHING_SERVICE = auto()
