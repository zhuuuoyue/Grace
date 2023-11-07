# -*- coding: utf-8 -*-

from typing import Any, List

from .filter import FilterX


def is_string_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    for item in value:
        if not isinstance(item, str):
            return False
    return True


def is_list_of(lst: List[Any], filter_func: FilterX) -> bool:
    if not isinstance(lst, list):
        return False
    if not isinstance(filter_func, FilterX):
        return False
    for item in lst:
        if not filter_func.filter(item):
            return False
    return True
