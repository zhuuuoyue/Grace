# -*- coding: utf-8 -*-

from typing import Optional, List, Union

from PySide6.QtCore import QObject, Slot, Signal, Property

from tasks.create import SolutionData, DocumentData, TemplateData, EditSolutionTasks, EditDocumentTasks, EditTemplateTasks


class EditCreationSolutionsModel(QObject):

    solutions_changed = Signal(type(List[SolutionData]))
    current_solution_changed = Signal(int)
    documents_changed = Signal(type(List[DocumentData]))
    current_document_changed = Signal(int)
    template_changed = Signal(type(Union[TemplateData, None]))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

        self.__solutions: List[SolutionData] = list()
        self.__current_solution: int = 0
        self.__documents: List[DocumentData] = list()
        self.__current_document: int = 0
        self.__template: Union[TemplateData, None] = None

    def initialize(self):
        # connect slots and signals
        self.solutions_changed.connect(self.__on_solutions_changed)
        self.current_solution_changed.connect(self.__on_current_solution_changed)
        self.documents_changed.connect(self.__on_documents_changed)
        self.current_document_changed.connect(self.__on_current_document_changed)

        # update members
        self.update()

    def update(self):
        self.solutions = EditSolutionTasks.get_solutions()

    # solutions

    def get_solutions(self) -> List[SolutionData]:
        return self.__solutions

    def set_solutions(self, value: List[SolutionData]):
        if self.solutions != value:
            self.__solutions = value
            self.solutions_changed.emit(self.solutions)

    solutions = Property(type(List[SolutionData]), fget=get_solutions, fset=set_solutions, notify=solutions_changed)

    # current_solution

    def get_current_solution(self) -> int:
        return self.__current_solution

    def set_current_solution(self, value: int):
        if self.current_solution != value:
            self.__current_solution = value
            self.current_solution_changed.emit(self.current_solution)

    current_solution = Property(int, fget=get_current_solution, fset=set_current_solution,
                                notify=current_solution_changed)

    # documents

    def get_documents(self) -> List[DocumentData]:
        return self.__documents

    def set_documents(self, value: List[DocumentData]):
        if self.documents != value:
            self.__documents = value
            self.documents_changed.emit(self.documents)

    documents = Property(type(List[DocumentData]), fget=get_documents, fset=set_documents, notify=documents_changed)

    # current_document

    def get_current_document(self) -> int:
        return self.__current_document

    def set_current_document(self, value: int):
        if self.current_document != value:
            self.__current_document = value
            self.current_document_changed.emit(self.current_document)

    current_document = Property(int, fget=get_current_document, fset=set_current_document,
                                notify=current_document_changed)

    # template

    def get_template(self) -> Union[TemplateData, None]:
        return self.__template

    def set_template(self, value: Union[TemplateData, None]):
        if self.template != value:
            self.__template = value
            self.template_changed.emit(self.template)

    template = Property(type(Union[TemplateData, None]), fget=get_template, fset=set_template, notify=template_changed)

    # slots

    @Slot(type(List[SolutionData]))
    def __on_solutions_changed(self, solutions: List[SolutionData]):
        if len(solutions) == 0:
            self.current_solution = 0
        else:
            self.current_solution = solutions[0].id

    @Slot(int)
    def __on_current_solution_changed(self, solution_id: int):
        if 0 == solution_id:
            self.documents = list()
        else:
            self.documents = EditSolutionTasks.get_documents_by_solution_id(solution_id)

    @Slot(type(List[DocumentData]))
    def __on_documents_changed(self, documents: List[DocumentData]):
        if len(documents) == 0:
            self.current_document = 0
        else:
            self.current_document = documents[0].id

    @Slot(int)
    def __on_current_document_changed(self, document_id: int):
        if 0 == document_id:
            self.template = None
        else:
            self.template = EditDocumentTasks.get_template_by_document_id(document_id)
