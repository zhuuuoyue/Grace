# -*- coding: utf-8 -*-

import os
import shutil
from typing import Optional, Sequence, List, Dict, Union
from xml.dom import minidom as xml_dom

from service import get_searcher, SearcherType, ISearcher
from common import is_string_list

from .concept import Environment


def detect_software_packages(
        include_architecture_software_package: Optional[bool] = True,
        include_structure_software_package: Optional[bool] = False) -> Sequence[str]:
    keywords: List[str] = list()
    if include_architecture_software_package:
        keywords.append('AppGarch.exe')
    if include_structure_software_package:
        keywords.append('AppGstr.exe')
    if len(keywords) == 0:
        return list()
    searcher: ISearcher = get_searcher(SearcherType.LOCAL_SEARCHER)
    search_result = searcher.search_exe('|'.join(keywords))
    result: List[str] = list()
    for search_result_item in search_result:
        result.append(os.path.dirname(search_result_item))
    return result


def environment_to_string(environment: Environment) -> str:
    if environment == Environment.A:
        return 'A'
    mapping: Dict[Environment, str] = {
        Environment.A: 'A',
        Environment.B: 'B',
        Environment.C: 'C',
        Environment.QA: 'QA',
        Environment.QA_STG: 'QS STG'
    }
    return mapping[environment] if environment in mapping else str()


def infer_environment(package_path: str) -> Union[Environment, None]:
    if not os.path.isdir(package_path):
        return
    file_path = os.path.join(package_path, 'gmepProjectSetting_config.xml')
    if not os.path.isfile(file_path):
        return
    tree = xml_dom.parse(file_path)
    root = tree.documentElement
    nodes = root.getElementsByTagName('env')
    if len(nodes) == 0:
        return
    first_node = nodes[0]
    if not isinstance(first_node, xml_dom.Element):
        return
    value = first_node.firstChild.data
    mapping: Dict[str, Environment] = {
        "production": Environment.A,
        "production-stg": Environment.B,
        "production-test": Environment.C,
        "qa": Environment.QA,
        "qastg": Environment.QA_STG
    }
    return None if value not in mapping else mapping[value]


class CleanDirectoriesResult(object):

    def __init__(self):
        self.succeeded: int = 0
        self.failed: int = 0


class CleanDirectories(object):

    def __init__(self, clean_list: Optional[List[str]] = None):
        self.__clean_list: List[str] = list()

        self.clean_list = clean_list

    @property
    def clean_list(self) -> List[str]:
        return self.__clean_list

    @clean_list.setter
    def clean_list(self, value: List[str]):
        if is_string_list(value):
            self.__clean_list = value

    def run(self) -> CleanDirectoriesResult:
        result = CleanDirectoriesResult()
        for dir_path in self.clean_list:
            if not os.path.isdir(dir_path):
                continue
            children = os.listdir(dir_path)
            for child in children:
                child_path = os.path.join(dir_path, child)
                if os.path.isdir(child_path):
                    shutil.rmtree(child_path)
                    if os.path.isdir(child_path):
                        result.failed += 1
                    else:
                        result.succeeded += 1
                elif os.path.isfile(child_path):
                    os.remove(child_path)
                    if os.path.isfile(child_path):
                        result.failed += 1
                    else:
                        result.succeeded += 1
        return result
