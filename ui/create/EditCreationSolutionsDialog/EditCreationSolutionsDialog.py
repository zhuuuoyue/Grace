# -*- coding: utf-8 -*-

from typing import Optional

from PySide6.QtCore import Slot, QModelIndex, QStringListModel
from PySide6.QtWidgets import QWidget

from tasks.create import EditSolutionTasks, SolutionData
from ui.basic.DialogBase import DialogBase

from ui.create.CreationSolutionEditor import CreationSolutionEditorDialog
from ui.create.CreationDocumentEditor import CreationDocumentEditorDialog

from .EditCreationSolutionsView import EditCreationSolutionsView
from .EditCreationSolutionsViewModel import EditCreationSolutionsViewModel


class EditCreationSolutionsDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(object_name='b870dbad-9d26-4d6f-8315-d4569ed635ed', parent=parent)
        self.__ui = EditCreationSolutionsView(self)
        self.__vm = EditCreationSolutionsViewModel(self)
        self.__ui.solution_list.setModel(self.__vm.solution_list_model)
        self.__ui.solution_list.setCurrentIndex(self.__vm.current_solution_index)

    def initialize(self):
        # connect slots and signals
        self.__ui.add_solution.clicked.connect(self.__on_add_solution_button_clicked)
        self.__ui.edit_solution.clicked.connect(self.__on_edit_solution_button_clicked)

        self.__ui.add_document.clicked.connect(self.__on_add_document_button_clicked)
        self.__ui.edit_document.clicked.connect(self.__on_edit_document_button_clicked)

        self.__vm.current_solution_index_changed.connect(self.__ui.solution_list.setCurrentIndex)

        # initialize members
        self.__vm.initialize()

    # dialog

    @Slot()
    def __on_add_solution_button_clicked(self):
        existing_solution_names = EditSolutionTasks.get_solution_names()
        dialog = CreationSolutionEditorDialog(existing_solution_names=existing_solution_names, parent=self)
        if 1 == dialog.exec():
            new_solution_name = dialog.get_solution_name()
            solution = EditSolutionTasks.add_solution(SolutionData(name=new_solution_name))
            self.__vm.update()
            self.__vm.switch_solution(solution)

    @Slot()
    def __on_delete_solution_button_clicked(self):
        pass

    @Slot()
    def __on_edit_solution_button_clicked(self):
        dialog = CreationSolutionEditorDialog(parent=self)
        if 1 == dialog.exec():
            new_solution_name = dialog.get_solution_name()
            EditSolutionTasks.update_solution(SolutionData(object_id=0, name=new_solution_name))

    @Slot()
    def __on_add_document_button_clicked(self):
        dialog = CreationDocumentEditorDialog(parent=self)
        if 1 == dialog.exec():
            pass

    @Slot()
    def __on_delete_document_button_clicked(self):
        pass

    @Slot()
    def __on_edit_document_button_clicked(self):
        dialog = CreationDocumentEditorDialog(parent=self)
        if 1 == dialog.exec():
            pass
