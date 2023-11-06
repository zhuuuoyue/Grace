# -*- coding: utf-8 -*-

from os.path import isfile
from typing import Union

from sqlalchemy import create_engine, Engine

from db.base import Base
from db.git import *


__engine: Union[Engine, None] = None


def initialize(db_path: str):
    global __engine
    __engine = create_engine(f'sqlite:///{db_path}')
    if not isfile(db_path):
        Base.metadata.create_all(__engine)


def get_engine() -> Union[Engine, None]:
    return __engine
