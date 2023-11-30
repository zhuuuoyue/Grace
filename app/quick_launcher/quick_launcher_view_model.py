# -*- coding: utf-8 -*-

from typing import Optional, Sequence, Union

from PySide6.QtCore import QObject, Slot, Signal, Property, QStringListModel, QModelIndex

from ui import WidgetViewModelBase

from .command_info import CommandInfo
from .quick_launcher_model import QuickLauncherModel


class QuickLauncherViewModel(WidgetViewModelBase):

    current_command_index_changed = Signal(QModelIndex)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__model = QuickLauncherModel(self)
        self.__candidate_model = QStringListModel(self)
        self.__current_command_index = self.create_index()

    @property
    def model(self) -> QuickLauncherModel:
        return self.__model

    @property
    def candidate_model(self) -> QStringListModel:
        return self.__candidate_model

    def get_current_command_index(self) -> QModelIndex:
        return self.__current_command_index

    def set_current_command_index(self, index: QModelIndex):
        if self.current_command_index != index:
            row = index.row()
            if row == -1 or (0 <= row < len(self.model.candidates)):
                self.__current_command_index = index
                self.current_command_index_changed.emit(self.current_command_index)

    current_command_index = Property(QModelIndex, fget=get_current_command_index, fset=set_current_command_index,
                                     notify=current_command_index_changed)

    def initialize(self):
        self.model.candidates_changed.connect(self.__on_model_candidates_changed)
        self.model.initialize()

    def update(self):
        self.model.update()

    def get_current_command(self) -> Union[str, None]:
        row = self.current_command_index.row()
        if row == -1:
            return None
        if 0 <= row < len(self.model.candidates):
            return self.model.candidates[row].command_id
        else:
            return None

    def update_keyword(self, keyword: str):
        self.model.set_keyword(keyword)

    def switch_to_next_command_option(self):
        self.move_command_selection(1)

    def switch_to_previous_command_option(self):
        self.move_command_selection(-1)

    def create_index(self, index: Optional[int] = -1) -> QModelIndex:
        return self.candidate_model.createIndex(index, 0)

    def move_command_selection(self, delta: int):
        row_index = self.current_command_index.row()
        if row_index == -1:
            return
        new_row_index = row_index + delta
        if 0 <= new_row_index < len(self.model.candidates):
            self.current_command_index = self.create_index(new_row_index)

    @Slot(type(Sequence[CommandInfo]))
    def __on_model_candidates_changed(self, candidates: Sequence[CommandInfo]):
        self.current_command_index = self.create_index()
        self.candidate_model.beginResetModel()
        self.candidate_model.setStringList([item.name for item in candidates])
        self.candidate_model.endResetModel()
        current_row = -1 if len(candidates) == 0 else 0
        self.current_command_index = self.create_index(current_row)
