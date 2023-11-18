# -*- coding: utf-8 -*-

from typing import List

from sqlalchemy.orm import Session

from db import get_engine
from db.create import EntEncoding, EntCreationTemplate

from .Encoding import Encoding
from .TemplateData import TemplateData
from .DocumentData import DocumentData


def get_encodings() -> List[Encoding]:
    with Session(get_engine()) as session:
        encoding_list = session.query(EntEncoding).order_by(EntEncoding.id).all()
        return [Encoding(id_value=item.id, name=item.name) for item in encoding_list]


def create_document(document: DocumentData):
    with Session(get_engine()) as session:
        created_template = EntCreationTemplate(
            id=document.id,
            template_id=document.template_id,
            relative_path=document.relative_path,
            encoding_id=document.encoding_id
        )
        session.add(created_template)
        session.commit()


def delete_document(template: TemplateData):
    with Session(get_engine()) as session:
        searched_template = session.query(EntCreationTemplate).filter(EntCreationTemplate.id == template.id).first()
        if searched_template is not None:
            session.delete(searched_template)
            session.commit()


def update_document():
    pass


def retrieve_documents() -> List[DocumentData]:
    with Session(get_engine()) as session:
        searched_templates = session.query(EntCreationTemplate).order_by(EntCreationTemplate.relative_path).all()
        return [
            DocumentData(
                document_id=searched_template.id,
                template_id=searched_template.template_id,
                encoding_id=searched_template.encoding_id,
                relative_path=searched_template.relative_path
            )
            for searched_template in searched_templates
        ]
