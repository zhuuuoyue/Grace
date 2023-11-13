# -*- coding: utf-8 -*-

import os
from enum import IntEnum, auto
from abc import ABC, abstractmethod
from typing import Union, Sequence, List

from everytools import EveryTools
from pandas import DataFrame


def data_frame_to_sequence(df: DataFrame) -> Sequence[str]:
    result: List[str] = list()
    for row in range(len(df)):
        full_path = os.path.join(df.iloc[row]['path'], df.iloc[row]['name'])
        result.append(full_path)
    return result


class SearcherType(IntEnum):

    LOCAL_SEARCHER = auto()
    SEARCHING_SERVICE = auto()


class ISearcher(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def search(self,
               keyword: str,
               match_path: bool = False,
               match_case: bool = False,
               match_whole_word: bool = False,
               use_regex: bool = False
               ) -> Sequence[str]:
        pass

    @abstractmethod
    def search_exe(self, keyword: str) -> Sequence[str]:
        pass

    @abstractmethod
    def search_doc(self, keyword: str) -> Sequence[str]:
        pass

    @abstractmethod
    def search_ext(self, ext: str, keyword: str) -> Sequence[str]:
        pass

    @abstractmethod
    def search_pic(self, keyword: str) -> Sequence[str]:
        pass

    @abstractmethod
    def search_audio(self, keyword: str) -> Sequence[str]:
        pass

    @abstractmethod
    def search_folder(self, keyword: str) -> Sequence[str]:
        pass

    @abstractmethod
    def search_in_located(self, path: str, keyword: str) -> Sequence[str]:
        pass

    @abstractmethod
    def search_video(self, keyword: str) -> Sequence[str]:
        pass

    @abstractmethod
    def search_zip(self, keyword: str) -> Sequence[str]:
        pass


class LocalSearcher(ISearcher):

    _searcher: Union[EveryTools, None] = None

    def __init__(self):
        super().__init__()
        if self._searcher is None:
            self._searcher = EveryTools()

    def search(self, keyword: str, match_path: bool = False, match_case: bool = False, match_whole_word: bool = False,
               use_regex: bool = False) -> Sequence[str]:
        self._searcher.search(keyword, math_path=match_path, math_case=match_case, whole_world=match_whole_word,
                              regex=use_regex)
        return data_frame_to_sequence(self._searcher.results())

    def search_exe(self, keyword: str) -> Sequence[str]:
        self._searcher.search_exe(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_doc(self, keyword: str) -> Sequence[str]:
        self._searcher.search_doc(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_ext(self, ext: str, keyword: str) -> Sequence[str]:
        self._searcher.search_ext(ext, keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_pic(self, keyword: str) -> Sequence[str]:
        self._searcher.search_pic(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_audio(self, keyword: str) -> Sequence[str]:
        self._searcher.search_audio(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_folder(self, keyword: str) -> Sequence[str]:
        self._searcher.search_folder(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_in_located(self, path: str, keyword: str) -> Sequence[str]:
        self._searcher.search_in_located(path, keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_video(self, keyword: str) -> Sequence[str]:
        self._searcher.search_video(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_zip(self, keyword: str) -> Sequence[str]:
        self._searcher.search_zip(keyword)
        return data_frame_to_sequence(self._searcher.results())


class SearchingService(ISearcher):

    def __init__(self):
        super().__init__()

    def search(self, keyword: str, match_path: bool = False, match_case: bool = False, match_whole_word: bool = False,
               use_regex: bool = False) -> Sequence[str]:
        pass

    def search_exe(self, keyword: str) -> Sequence[str]:
        pass

    def search_doc(self, keyword: str) -> Sequence[str]:
        pass

    def search_ext(self, ext: str, keyword: str) -> Sequence[str]:
        pass

    def search_pic(self, keyword: str) -> Sequence[str]:
        pass

    def search_audio(self, keyword: str) -> Sequence[str]:
        pass

    def search_folder(self, keyword: str) -> Sequence[str]:
        pass

    def search_in_located(self, path: str, keyword: str) -> Sequence[str]:
        pass

    def search_video(self, keyword: str) -> Sequence[str]:
        pass

    def search_zip(self, keyword: str) -> Sequence[str]:
        pass


def get_searcher(searcher_type: SearcherType = SearcherType.LOCAL_SEARCHER) -> ISearcher:
    if SearcherType.LOCAL_SEARCHER == searcher_type:
        return LocalSearcher()
    elif SearcherType.SEARCHING_SERVICE == searcher_type:
        return SearchingService()
