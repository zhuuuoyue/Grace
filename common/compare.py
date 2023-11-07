# -*- coding: utf-8 -*-

from typing import Any, List


def are_same_lists(a: List[Any], b: List[Any]) -> bool:
    if not isinstance(a, list) or not isinstance(b, list):
        return False
    if len(a) != len(b):
        return False
    for a_item, b_item in zip(a, b):
        if a_item != b_item:
            return False
    return True


def are_same_string_lists(a: Any, b: Any) -> bool:
    if not isinstance(a, list) or not isinstance(b, list):
        return False
    if len(a) != len(b):
        return False
    for a_item, b_item in zip(a, b):
        if not isinstance(a_item, str) or not isinstance(b_item, str):
            return False
        if a_item != b_item:
            return False
    return True
