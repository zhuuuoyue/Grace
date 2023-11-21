# -*- coding: utf-8 -*-

from typing import Optional, List

from PySide6.QtCore import Qt, QObject, QStringListModel, QModelIndex, Slot, Signal, Property

from tasks.create import SolutionData

from .EditCreationSolutionsModel import EditCreationSolutionsModel


class EditCreationSolutionsViewModel(QObject):

    current_solution_index_changed = Signal(QModelIndex)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

        self.__model = EditCreationSolutionsModel(self)

        self.__solution_list_model = QStringListModel()
        self.__current_solution_index: QModelIndex = self.create_solution_index()

    def initialize(self):
        # connect slots and signals
        self.__model.solutions_changed.connect(self.__on_vm_solutions_changed, type=Qt.ConnectionType.DirectConnection)
        self.__model.current_solution_changed.connect(self.__on_vm_current_solution_changed, type=Qt.ConnectionType.DirectConnection)

        # initialize members
        self.model.initialize()

    def update(self):
        self.model.update()

    def get_model(self) -> EditCreationSolutionsModel:
        return self.__model

    model = property(fget=get_model)

    def get_solution_list_model(self) -> QStringListModel:
        return self.__solution_list_model

    solution_list_model = property(fget=get_solution_list_model)

    # properties

    def get_current_solution_index(self) -> QModelIndex:
        return self.__current_solution_index

    def set_current_solution_index(self, value: QModelIndex):
        if self.current_solution_index != value:
            self.__current_solution_index = value
            self.current_solution_index_changed.emit(self.current_solution_index)

    current_solution_index = Property(QModelIndex, fget=get_current_solution_index, fset=set_current_solution_index,
                                      notify=current_solution_index_changed)

    # utils

    def create_solution_index(self, index: Optional[int] = -1) -> QModelIndex:
        return self.__solution_list_model.createIndex(index, 0)

    # public

    def switch_solution(self, solution_data: SolutionData):
        self.model.current_solution = solution_data.id

    # slots

    @Slot(type(List[SolutionData]))
    def __on_vm_solutions_changed(self, solutions: List[SolutionData]):
        items = [item.name for item in solutions]
        self.__solution_list_model.beginResetModel()
        self.__solution_list_model.setStringList(items)
        self.__solution_list_model.endResetModel()

    @Slot(int)
    def __on_vm_current_solution_changed(self, solution_id: int):
        for index, solution in enumerate(self.model.solutions):
            if solution_id == solution.id:
                self.current_solution_index = self.create_solution_index(index)
                break
