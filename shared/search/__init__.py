# -*- coding: utf-8 -*-

__all__ = ['Searcher', 'get_searcher', 'SearcherType']

from .searcher import Searcher
from .local_searcher import LocalSearcher
from .searching_service import SearchingService
from .searcher_type import SearcherType


def get_searcher(searcher_type_: SearcherType = SearcherType.LOCAL_SEARCHER) -> Searcher:
    if SearcherType.LOCAL_SEARCHER == searcher_type_:
        return LocalSearcher()
    elif SearcherType.SEARCHING_SERVICE == searcher_type_:
        return SearchingService()
