# -*- coding: utf-8 -*-

__all__ = ['DirectoryInformation']


class DirectoryInformation(object):

    def __init__(self, dir_path: str, checked: bool):
        self.path: str = dir_path
        self.checked: bool = checked

    def __eq__(self, other) -> bool:
        if not isinstance(other, DirectoryInformation):
            return False
        return self.path == other.path and self.checked == other.checked
