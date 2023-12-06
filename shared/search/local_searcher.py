# -*- coding: utf-8 -*-

__all__ = ['LocalSearcher']

from typing import Union

from everytools import EveryTools

from .searcher import Searcher
from .search_result import SearchResult
from .utils import data_frame_to_sequence


class LocalSearcher(Searcher):

    _searcher: Union[EveryTools, None] = None

    def __init__(self):
        super().__init__()
        if self._searcher is None:
            self._searcher = EveryTools()

    def search(self, keyword: str, match_path: bool = False, match_case: bool = False, match_whole_word: bool = False,
               use_regex: bool = False) -> SearchResult:
        self._searcher.search(keyword, math_path=match_path, math_case=match_case, whole_world=match_whole_word,
                              regex=use_regex)
        return data_frame_to_sequence(self._searcher.results())

    def search_exe(self, keyword: str) -> SearchResult:
        self._searcher.search_exe(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_doc(self, keyword: str) -> SearchResult:
        self._searcher.search_doc(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_ext(self, ext: str, keyword: str) -> SearchResult:
        self._searcher.search_ext(ext, keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_pic(self, keyword: str) -> SearchResult:
        self._searcher.search_pic(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_audio(self, keyword: str) -> SearchResult:
        self._searcher.search_audio(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_folder(self, keyword: str) -> SearchResult:
        self._searcher.search_folder(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_in_located(self, path: str, keyword: str) -> SearchResult:
        self._searcher.search_in_located(path, keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_video(self, keyword: str) -> SearchResult:
        self._searcher.search_video(keyword)
        return data_frame_to_sequence(self._searcher.results())

    def search_zip(self, keyword: str) -> SearchResult:
        self._searcher.search_zip(keyword)
        return data_frame_to_sequence(self._searcher.results())
