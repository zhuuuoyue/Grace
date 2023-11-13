# -*- coding: utf-8 -*-

import os
from typing import Optional, Sequence, List, Dict, Union
from xml.dom import minidom as xml_dom

from service import get_searcher, SearcherType, ISearcher

from .concept import Environment


def detect_software_packages(arch: Optional[bool] = True, stru: Optional[bool] = False) -> Sequence[str]:
    keywords: List[str] = list()
    if arch:
        keywords.append('AppGarch.exe')
    if stru:
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


def switch_environment(package_path: str, target_environment: Environment) -> bool:
    pass
