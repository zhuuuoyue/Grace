# -*- coding: utf-8 -*-

__all__ = ['SearchResult', 'SearchResultItem']

import re
from typing import List, Sequence, Union, Self, Any, Callable

_RECYCLE_BIN_PATH_PATTERN = re.compile(r'\w:\\\$RECYCLE\.BIN\\.*')


class SearchResultItem(object):

    def __init__(self, name: str, path: str, size: int, created_date: str, modified_date: str, file_extension: str,
                 is_file: bool, is_folder: bool, is_volume: bool):
        self.name = name
        self.path = path
        self.size = size
        self.created_date = created_date
        self.modified_date = modified_date
        self.file_extension = file_extension
        self.is_file = is_file
        self.is_folder = is_folder
        self.is_volume = is_volume


def in_recycle_bin(item: SearchResultItem) -> bool:
    matched = re.match(_RECYCLE_BIN_PATH_PATTERN, item.path)
    return matched is not None


class SearchResult(object):

    def __init__(self, items: List[SearchResultItem]):
        self.__items: List[SearchResultItem] = items

    def all(self) -> List[SearchResultItem]:
        return self.__items

    def first(self) -> Union[SearchResultItem, None]:
        return None if len(self.__items) == 0 else self.__items[0]

    def retrieve(self, func: Callable[[SearchResultItem], Any]) -> Sequence[Any]:
        return [func(item) for item in self.__items]

    def retrieve_filenames(self) -> Sequence[str]:
        return [item.name for item in self.__items]

    def retrieve_paths(self) -> Sequence[str]:
        return [item.path for item in self.__items]

    def filter(self, func: Callable[[SearchResultItem], bool]) -> Self:
        self.__items = [item for item in filter(func, self.__items)]
        return self

    def remove_items_in_recycle_bin(self) -> Self:
        return self.filter(lambda item: not in_recycle_bin(item))

    def remove_files(self) -> Self:
        return self.filter(lambda item: not item.is_file)

    def remove_folders(self) -> Self:
        return self.filter(lambda item: not item.is_folder)

    def order_by(self, func: Callable[[SearchResultItem], Any]) -> Self:
        self.__items.sort(key=func)
        return self

    def order_by_filename(self) -> Self:
        return self.order_by(lambda item: item.name)

    def order_by_path(self) -> Self:
        return self.order_by(lambda item: item.path)

    def reverse(self) -> Self:
        self.__items.reverse()
        return self
