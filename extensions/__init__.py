# -*- coding: utf-8 -*-

import os
from enum import IntEnum, auto
from typing import List, Sequence, Union, Optional
from importlib import import_module

from PySide6.QtWidgets import QTableWidget, QWidget, QDialog, QVBoxLayout, QTableWidgetItem

from service.context import Context


class ExtensionType(IntEnum):
    UNKNOWN = auto()
    MODULE = auto()
    PACKAGE = auto()


class LoadingResult(object):

    def __init__(self):
        self.name: str = ''
        self.type: ExtensionType = ExtensionType.UNKNOWN
        self.error: Union[Exception, None] = None


class LoadingResultDialog(QDialog):

    def __init__(self, result: Sequence[LoadingResult], parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__initialize()
        self.__load_data(result)

    def __initialize(self):
        self.setWindowTitle('Loading modules and packages')
        self.setMinimumSize(400, 320)
        self.__table = QTableWidget()
        self.__table.setColumnCount(4)
        self.__table.setHorizontalHeaderLabels(['State', 'Type', 'Name', 'Error Information'])
        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.__table)
        self.setLayout(self.__layout)

    def __load_data(self, data: Sequence[LoadingResult]):
        self.__table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            state = 'Succeeded' if row_data.error is None else 'Failed'
            self.__table.setItem(row_index, 0, QTableWidgetItem(state))
            t: str = ''
            if row_data.type == ExtensionType.MODULE:
                t = 'Module'
            elif row_data.type == ExtensionType.PACKAGE:
                t = 'Package'
            self.__table.setItem(row_index, 1, QTableWidgetItem(t))
            self.__table.setItem(row_index, 2, QTableWidgetItem(row_data.name))
            err_info: str = ''
            if isinstance(row_data.error, Exception):
                err_info = str(row_data.error)
            self.__table.setItem(row_index, 3, QTableWidgetItem(err_info))


def initialize(ctx: Context):
    # loading
    loading_result: List[LoadingResult] = list()
    children = os.listdir(__path__[0])
    for child in children:
        full_path = f'{__path__[0]}\\{child}'
        loading: LoadingResult = LoadingResult()
        loading.type = ExtensionType.UNKNOWN
        if os.path.isfile(full_path):
            if full_path == __file__:
                continue
            if child.lower().endswith('.py') and len(child) > 3:
                loading.type = ExtensionType.MODULE
        elif os.path.isdir(full_path):
            if os.path.isfile(f'{full_path}\\__init__.py'):
                loading.type = ExtensionType.PACKAGE
        if loading.type == ExtensionType.UNKNOWN:
            continue
        loading.name = child
        if loading.type == ExtensionType.MODULE:
            loading.name, ext = os.path.splitext(child)
        try:
            module_or_package = import_module(f'{__package__}.{loading.name}')
            try:
                module_or_package.initialize(ctx)
            except AttributeError as e:
                loading.error = e
        except ModuleNotFoundError as e:
            loading.error = e
        loading_result.append(loading)

    # show result
    errors: List[LoadingResult] = list()
    for loading in loading_result:
        if loading.error is not None:
            errors.append(loading)
    if len(errors) != 0:
        table = LoadingResultDialog(errors, ctx.main_window)
        table.show()
