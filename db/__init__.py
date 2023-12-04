# -*- coding: utf-8 -*-

import os
from typing import Union, NoReturn

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from events import ApplicationWillInit
from shared import get_context

from .TableBase import TableBase
from .create import (EntEncoding, EntCreationTemplate, EntCreationDocument, EntCreationSolution,
                     RelCreationSolutionAndDocument)


__engine: Union[Engine, None] = None


def get_engine() -> Union[Engine, None]:
    return __engine


def initialize_encoding_table(session: Session):
    encoding_ascii = EntEncoding(name='ASCII')
    encoding_utf_8 = EntEncoding(name='UTF-8')
    encoding_utf_8_with_bom = EntEncoding(name='UTF-8 with BOM')
    session.add_all([encoding_ascii, encoding_utf_8, encoding_utf_8_with_bom])
    session.commit()


class InitializeDBFile(ApplicationWillInit):

    def __init__(self):
        super().__init__()

    def exec(self, *args, **kwargs) -> NoReturn:
        db_path = get_context().data_file_path
        global __engine
        __engine = create_engine(f'sqlite:///{db_path}', echo_pool=True)

        if not os.path.isfile(db_path):
            TableBase.metadata.create_all(__engine)

            with Session(__engine) as session:
                initialize_encoding_table(session)


def initialize():
    InitializeDBFile()
