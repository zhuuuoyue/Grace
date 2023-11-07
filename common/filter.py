# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any


class FilterX(ABC):

    @abstractmethod
    def filter(self, obj: Any) -> bool:
        pass
