# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .TableBase import TableBase


class EntEncoding(TableBase):

    __tablename__ = 'ent_encoding'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    def __repr__(self):
        return f'EntEncoding(id={self.id!r}, name={self.name!r})'


class EntCreationTemplate(TableBase):

    __tablename__ = 'ent_creation_template'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    content: Mapped[str]

    def __repr__(self):
        return f'EntCreationTemplate(id={self.id!r}, name={self.name!r}, content={self.content!r})'


class EntCreationDocument(TableBase):

    __tablename__ = 'ent_creation_document'

    id: Mapped[int] = mapped_column(primary_key=True)
    relative_path: Mapped[str]
    template_id: Mapped[int] = mapped_column(ForeignKey('ent_creation_template.id'))
    encoding_id: Mapped[int] = mapped_column(ForeignKey('ent_encoding.id'))

    def __repr__(self):
        return f'EntCreationDocument(id={self.id!r}, relative_path={self.relative_path!r}, template_id={self.template_id!r}, encoding_id={self.encoding_id!r})'


class EntCreationSolution(TableBase):

    __tablename__ = 'ent_creation_solution'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))

    def __repr__(self):
        return f'EntCreationSolution(id={self.id!r}, name={self.name!r})'


class RelCreationSolutionAndDocument(TableBase):

    __tablename__ = 'rel_creation_solution_and_document'

    id: Mapped[int] = mapped_column(primary_key=True)
    solution_id: Mapped[int] = mapped_column(ForeignKey('ent_creation_solution.id'))
    document_id: Mapped[int] = mapped_column(ForeignKey('ent_creation_document.id'))

    def __repr__(self):
        return f'RelCreationSolutionAndDocument(id={self.id!r}, solution_id={self.solution_id!r}, document_id={self.document_id!r})'
