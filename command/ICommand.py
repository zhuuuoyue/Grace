# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class ICommand(ABC):

    @abstractmethod
    def exec(self, *args, **kwargs):
        pass
