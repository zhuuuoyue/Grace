# -*- coding: utf-8 -*-

__all__ = ['initialize_context', 'get_context']

from typing import Union

from .context import Context


__context: Union[Context, None] = None


def initialize_context(root_directory: str):
    global __context
    if __context is None:
        __context = Context(root_directory=root_directory)


def get_context() -> Context:
    return __context
