# -*- coding: utf-8 -*-

from typing import Set, List, Sequence, Union

from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_engine
from db.create import EntCreationTemplate

from .TemplateData import TemplateData


def add_template(template: TemplateData) -> bool:
    if len(template.name) == 0:
        return False
    with Session(get_engine()) as session:
        # query existing
        query_existing = select(EntCreationTemplate.name).where(EntCreationTemplate.name == template.name)
        existing = session.scalars(query_existing)
        if len(existing.all()) > 0:
            return False

        # insert
        ent_template = EntCreationTemplate(name=template.name, content=template.content)
        session.add(ent_template)
        session.commit()
    return True


def add_templates(templates: Sequence[TemplateData]) -> int:
    succeeded_count = 0
    with Session(get_engine()) as session:
        to_insert: List[EntCreationTemplate] = list()
        for template in templates:
            # validate template
            if len(template.name) == 0:
                continue

            # query existing
            query_existing = select(EntCreationTemplate.name).where(EntCreationTemplate.name == template.name)
            existing = session.scalars(query_existing)
            if len(existing.all()) > 0:
                continue

            # create entity
            ent_template = EntCreationTemplate(name=template.name, content=template.content)
            to_insert.append(ent_template)
            succeeded_count += 1

        session.add_all(to_insert)
        session.commit()
    return succeeded_count


def copy_and_insert_template(template: TemplateData) -> TemplateData:
    template_names = get_template_names()
    suffix = 1
    while True:
        new_template_name = f'{template.name}-{suffix}'
        if new_template_name not in template_names:
            template.name = new_template_name
            break
        suffix += 1
    add_template(template)
    return template


def delete_template(template_name: str) -> bool:
    with Session(get_engine()) as session:
        templates = session.query(EntCreationTemplate).filter(EntCreationTemplate.name == template_name).all()
        for template in templates:
            session.delete(template)
        session.commit()
    return True


def update_template(template_name: str, template_data: TemplateData) -> bool:
    with Session(get_engine()) as session:
        templates = session.query(EntCreationTemplate).filter(EntCreationTemplate.name == template_name).all()
        for template in templates:
            template.name = template_data.name
            template.content = template_data.content
        session.commit()
    return True


def has_template(template_name: str) -> bool:
    with Session(get_engine()) as session:
        sql = select(EntCreationTemplate.name).where(EntCreationTemplate.name == template_name)
        result = session.scalars(sql)
        return len(result.all()) > 0


def get_template_names() -> Set[str]:
    with Session(get_engine()) as session:
        template_names = session.scalars(select(EntCreationTemplate.name))
        return set(template_names)


def get_template_content_using_name(name: str) -> Union[str, None]:
    pass


def get_templates() -> Sequence[TemplateData]:
    with Session(get_engine()) as session:
        templates = session.scalars(select(EntCreationTemplate))
        result = list()
        for template in templates:
            result.append(TemplateData(id_value=template.id, name=template.name, content=template.content))
        return result


def get_template_by_id(template_id: int) -> Union[TemplateData, None]:
    with Session(get_engine()) as session:
        template = session.query(EntCreationTemplate).where(EntCreationTemplate.id == template_id).first()
        if template is not None:
            return TemplateData(id_value=template.id, name=template.name, content=template.content)
