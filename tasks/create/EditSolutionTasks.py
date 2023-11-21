# -*- coding: utf-8 -*-

from typing import Set, List, Union

from sqlalchemy.orm import Session

from db import get_engine
from db.create import EntCreationDocument, EntCreationSolution, RelCreationSolutionAndDocument

from .DocumentData import DocumentData
from .SolutionData import SolutionData


def get_solution_names() -> Set[str]:
    with Session(get_engine()) as session:
        items = session.query(EntCreationSolution.name).all()
        result = set()
        for item in items:
            result.add(item.name)
        return result


def get_solutions() -> List[SolutionData]:
    with Session(get_engine()) as session:
        items = session.query(EntCreationSolution).order_by(EntCreationSolution.name).all()
        result: List[SolutionData] = list()
        for item in items:
            solution_data = SolutionData(object_id=item.id, name=item.name)
            result.append(solution_data)
        return result


def add_solution(solution_data: SolutionData) -> SolutionData:
    with Session(get_engine()) as session:
        solution = EntCreationSolution(name=solution_data.name)
        session.add(solution)
        session.commit()
        solution = session.query(EntCreationSolution).where(EntCreationSolution.name == solution_data.name).first()
        return SolutionData(object_id=solution.id, name=solution.name)


def update_solution(solution_data: SolutionData):
    with Session(get_engine()) as session:
        item = session.query(EntCreationSolution).filter(EntCreationSolution.id == solution_data.id).first()
        if item is not None:
            item.name = solution_data.name
            session.commit()


def delete_solution(solution_data: SolutionData):
    pass


def get_document_by_id(document_id: int) -> Union[DocumentData, None]:
    return


def get_documents_by_solution_id(solution_id: int) -> List[DocumentData]:
    with (Session(get_engine()) as session):
        document_ids = session \
            .query(RelCreationSolutionAndDocument.document_id) \
            .where(RelCreationSolutionAndDocument.solution_id == solution_id).all()
        result: List[DocumentData] = list()
        for document_id in document_ids:
            document_ent = session.query(EntCreationDocument).where(EntCreationDocument.id == document_id).first()
            if document_ent is not None:
                document_obj = DocumentData(
                    document_id=document_ent.id,
                    relative_path=document_ent.relative_path,
                    template_id=document_ent.template_id,
                    encoding_id=document_ent.encoding_id
                )
                result.append(document_obj)
        return result
