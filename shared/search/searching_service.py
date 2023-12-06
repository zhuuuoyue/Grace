# -*- coding: utf-8 -*-

__all__ = ['SearchingService']

from .searcher import Searcher
from .search_result import SearchResult


class SearchingService(Searcher):

    def __init__(self):
        super().__init__()

    def search(self, keyword: str, match_path: bool = False, match_case: bool = False, match_whole_word: bool = False,
               use_regex: bool = False) -> SearchResult:
        pass

    def search_exe(self, keyword: str) -> SearchResult:
        pass

    def search_doc(self, keyword: str) -> SearchResult:
        pass

    def search_ext(self, ext: str, keyword: str) -> SearchResult:
        pass

    def search_pic(self, keyword: str) -> SearchResult:
        pass

    def search_audio(self, keyword: str) -> SearchResult:
        pass

    def search_folder(self, keyword: str) -> SearchResult:
        pass

    def search_in_located(self, path: str, keyword: str) -> SearchResult:
        pass

    def search_video(self, keyword: str) -> SearchResult:
        pass

    def search_zip(self, keyword: str) -> SearchResult:
        pass
