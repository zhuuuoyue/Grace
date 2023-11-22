# -*- coding: utf-8 -*-

from typing import Sequence

from ui import ApplicationBase


class Application(ApplicationBase):

    def __init__(self, args: Sequence[str]):
        super().__init__(args)
