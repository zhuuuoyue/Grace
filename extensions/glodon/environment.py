# -*- coding: utf-8 -*-

__all__ = ['Environment', 'environment_to_string', 'infer_environment']

import os
from typing import Dict, Union
from enum import IntEnum, auto
from xml.dom import minidom as xml_dom


class Environment(IntEnum):

    A = auto()
    B = auto()
    C = auto()
    QA = auto()
    QA_STG = auto()


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
    first_child = first_node.firstChild
    if first_child is None:
        return
    value = first_child.data
    mapping: Dict[str, Environment] = {
        "production": Environment.A,
        "production-stg": Environment.B,
        "production-test": Environment.C,
        "qa": Environment.QA,
        "qastg": Environment.QA_STG
    }
    return None if value not in mapping else mapping[value]
