# -*- coding: utf-8 -*-

import re
from copy import deepcopy
from typing import Set, Dict

from .TemplateData import TemplateData
from .SolutionData import SolutionData
from .Encoding import Encoding

_PARAMETER_PATTERN = re.compile(r'\$\{(\w[\w\d]*)\}')


def extract_parameters(content: str) -> Set[str]:
    parameters = re.findall(_PARAMETER_PATTERN, content)
    return set(parameters)


def complete_template(content: str, parameters: Dict[str, str]) -> str:
    filled = deepcopy(content)
    for key in parameters:
        value = parameters[key]
        if len(value) != 0:
            filled = filled.replace(f'${{{key}}}', parameters[key])
    return filled
