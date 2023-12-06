# -*- coding: utf-8 -*-

import os
from typing import List

from pandas import DataFrame

from .search_result import SearchResult, SearchResultItem


def data_frame_to_sequence(df: DataFrame) -> SearchResult:
    result: List[SearchResultItem] = list()
    for row in range(len(df)):
        item = df.iloc[row]
        result.append(
            SearchResultItem(
                name=item['name'],
                path=item['path'],
                size=int(item['size']),
                created_date=item['created_date'],
                modified_date=item['modified_date'],
                file_extension=item['file_extension'],
                is_file=bool(item['is_file']),
                is_folder=bool(item['is_folder']),
                is_volume=bool(item['is_volume'])
            )
        )
    return SearchResult(result)
