# -*- coding: utf-8 -*-

import os
import shutil
from typing import List, Optional

from common import is_string_list


class CleanDirectoriesResult(object):

    def __init__(self):
        self.succeeded: int = 0
        self.failed: int = 0


class CleanDirectories(object):

    def __init__(self, clean_list: Optional[List[str]] = None):
        self.__clean_list: List[str] = list()

        self.clean_list = clean_list

    @property
    def clean_list(self) -> List[str]:
        return self.__clean_list

    @clean_list.setter
    def clean_list(self, value: List[str]):
        if is_string_list(value):
            self.__clean_list = value

    def run(self) -> CleanDirectoriesResult:
        result = CleanDirectoriesResult()
        for dir_path in self.clean_list:
            if not os.path.isdir(dir_path):
                continue
            children = os.listdir(dir_path)
            for child in children:
                child_path = os.path.join(dir_path, child)
                if os.path.isdir(child_path):
                    shutil.rmtree(child_path)
                    if os.path.isdir(child_path):
                        result.failed += 1
                    else:
                        result.succeeded += 1
                elif os.path.isfile(child_path):
                    os.remove(child_path)
                    if os.path.isfile(child_path):
                        result.failed += 1
                    else:
                        result.succeeded += 1
        return result
