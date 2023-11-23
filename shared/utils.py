# -*- coding: utf-8 -*-

import os
import shutil
from typing import Sequence


def clean_directory(directory: str):
    if os.path.isdir(directory):
        children = os.listdir(directory)
        for child in children:
            child_path = os.path.join(directory, child)
            if os.path.isdir(child_path):
                shutil.rmtree(child_path)
            elif os.path.isfile(child_path):
                os.remove(child_path)


def clean_directories(directories: Sequence[str]):
    for directory in directories:
        clean_directory(directory)
