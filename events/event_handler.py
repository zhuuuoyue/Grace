# -*- coding: utf-8 -*-

__all__ = ['EventHandler']

from abc import ABC, abstractmethod
from typing import NoReturn


class EventHandler(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def exec(self, *args, **kwargs) -> NoReturn:
        pass
