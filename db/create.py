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


class EntTemplate(TableBase):

    __tablename__ = 'ent_template'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    content: Mapped[str]


class EntCreationTemplate(TableBase):

    __tablename__ = 'ent_creation_template'

    id: Mapped[int] = mapped_column(primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey('ent_template.id'))
    relative_path: Mapped[str]
    encoding_id: Mapped[int] = mapped_column(ForeignKey('ent_encoding.id'))


class EntCreationSolution(TableBase):

    __tablename__ = 'ent_creation_solution'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))


class RelCreationSolutionAndTemplate(TableBase):

    __tablename__ = 'rel_creation_solution_and_template'

    id: Mapped[int] = mapped_column(primary_key=True)
    creation_solution_id: Mapped[int] = mapped_column(ForeignKey('ent_creation_solution.id'))
    creation_template_id: Mapped[int] = mapped_column(ForeignKey('ent_creation_template.id'))
