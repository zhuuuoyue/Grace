# -*- coding: utf-8 -*-

from typing import List, Union

from sqlalchemy.orm import Session

from db import get_engine
from db.create import EntEncoding, EntCreationDocument

from .Encoding import Encoding
from .TemplateData import TemplateData
from .DocumentData import DocumentData
from tasks.create import EditTemplateTasks


def get_encodings() -> List[Encoding]:
    with Session(get_engine()) as session:
        encoding_list = session.query(EntEncoding).order_by(EntEncoding.id).all()
        return [Encoding(id_value=item.id, name=item.name) for item in encoding_list]


def create_document(document: DocumentData):
    with Session(get_engine()) as session:
        created_template = EntCreationDocument(
            id=document.id,
            template_id=document.template_id,
            relative_path=document.relative_path,
            encoding_id=document.encoding_id
        )
        session.add(created_template)
        session.commit()


def delete_document(template: TemplateData):
    with Session(get_engine()) as session:
        searched_template = session.query(EntCreationDocument).filter(EntCreationDocument.id == template.id).first()
        if searched_template is not None:
            session.delete(searched_template)
            session.commit()


def update_document():
    pass


def retrieve_documents() -> List[DocumentData]:
    with Session(get_engine()) as session:
        searched_templates = session.query(EntCreationDocument).order_by(EntCreationDocument.relative_path).all()
        return [
            DocumentData(
                document_id=searched_template.id,
                template_id=searched_template.template_id,
                encoding_id=searched_template.encoding_id,
                relative_path=searched_template.relative_path
            )
            for searched_template in searched_templates
        ]


def get_template_by_document_id(document_id: int) -> Union[TemplateData, None]:
    with Session(get_engine()) as session:
        document = session.query(EntCreationDocument).where(EntCreationDocument.id == document_id).first()
        if document is not None:
            return EditTemplateTasks.get_template_by_id(document.template_id)
