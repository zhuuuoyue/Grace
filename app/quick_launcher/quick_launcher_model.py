# -*- coding: utf-8 -*-

from typing import Optional, Sequence, List

from PySide6.QtCore import QObject, Signal, Slot, Property

from ui import WidgetModelBase
from command import get_quick_commands

from .command_info import CommandInfo


class QuickLauncherModel(WidgetModelBase):

    all_items_changed = Signal(type(Sequence[CommandInfo]))
    keyword_changed = Signal(type(str))
    candidates_changed = Signal(type(Sequence[CommandInfo]))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__all_items: Sequence[CommandInfo] = list()
        self.__keyword: str = str()
        self.__candidates: Sequence[CommandInfo] = list()

    def get_all_items(self) -> Sequence[CommandInfo]:
        return self.__all_items

    def set_all_items(self, value: Sequence[CommandInfo]):
        if self.all_items != value:
            self.__all_items = value
            self.all_items_changed.emit(self.all_items)

    all_items = Property(type(Sequence[CommandInfo]), fget=get_all_items, fset=set_all_items, notify=all_items_changed)

    def get_keyword(self) -> str:
        return self.__keyword

    def set_keyword(self, value: str):
        if self.keyword != value:
            self.__keyword = value
            self.keyword_changed.emit(self.keyword)

    keyword = Property(type(str), fget=get_keyword, fset=set_keyword, notify=keyword_changed)

    def get_candidates(self) -> Sequence[CommandInfo]:
        return self.__candidates

    def set_candidates(self, value: Sequence[CommandInfo]):
        if self.candidates != value:
            self.__candidates = value
            self.candidates_changed.emit(self.candidates)

    candidates = Property(type(Sequence[CommandInfo]), fget=get_candidates, fset=set_candidates,
                          notify=candidates_changed)

    def initialize(self):
        self.all_items_changed.connect(self.__on_all_items_changed)
        self.keyword_changed.connect(self.__on_keyword_changed)

        quick_commands = get_quick_commands()
        all_items = [CommandInfo(name=command[0], command_id=command[1]) for command in quick_commands]
        all_items.sort()
        self.all_items = all_items

    def update(self):
        pass

    def __update_candidates(self):
        if len(self.keyword) == 0:
            self.candidates = self.all_items
        else:
            lower_keyword = self.keyword.lower()
            candidates: List[CommandInfo] = list()
            for item in self.all_items:
                lower_candidate = item.name.lower()
                index = lower_candidate.find(lower_keyword)
                if -1 != index:
                    candidates.append(item)
            self.candidates = candidates

    @Slot(type(Sequence[CommandInfo]))
    def __on_all_items_changed(self, all_items: Sequence[CommandInfo]):
        self.__update_candidates()

    @Slot(str)
    def __on_keyword_changed(self, keyword: str):
        self.__update_candidates()
