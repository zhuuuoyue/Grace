# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class TableBase(Base):

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement='auto')
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)
    deleted = Column(Boolean)


class EntTableBase(TableBase):

    __abstract__ = True


class RelTableBase(TableBase):

    __abstract__ = True
