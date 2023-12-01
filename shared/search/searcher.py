# -*- coding: utf-8 -*-

__all__ = ['Searcher']

from abc import ABC, abstractmethod
from typing import Sequence


class Searcher(ABC):

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


