# -*- coding: utf-8 -*-

import os
from typing import Union

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from db.TableBase import TableBase
from .create import EntEncoding, EntTemplate, EntCreationTemplate, EntCreationSolution, RelCreationSolutionAndTemplate


__engine: Union[Engine, None] = None


def initialize_encoding_table(session: Session):
    encoding_ascii = EntEncoding(name='ASCII')
    encoding_utf_8 = EntEncoding(name='UTF-8')
    encoding_utf_8_with_bom = EntEncoding(name='UTF-8 with BOM')
    session.add_all([encoding_ascii, encoding_utf_8, encoding_utf_8_with_bom])
    session.commit()


def initialize(db_path: str):
    global __engine
    __engine = create_engine(f'sqlite:///{db_path}', echo_pool=True)

    if not os.path.isfile(db_path):
        TableBase.metadata.create_all(__engine)

        with Session(__engine) as session:
            initialize_encoding_table(session)


def get_engine() -> Union[Engine, None]:
    return __engine
