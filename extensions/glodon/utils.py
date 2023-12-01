# -*- coding: utf-8 -*-

import os
from typing import Optional, Sequence, List

from shared import get_searcher, SearcherType, Searcher


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
    searcher: Searcher = get_searcher(SearcherType.LOCAL_SEARCHER)
    search_result = searcher.search_exe('|'.join(keywords))
    result: List[str] = list()
    for search_result_item in search_result:
        result.append(os.path.dirname(search_result_item))
    return result
