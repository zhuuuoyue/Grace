# -*- coding: utf-8 -*-

import os
from typing import Sequence, List

from pandas import DataFrame


def data_frame_to_sequence(df: DataFrame) -> Sequence[str]:
    result: List[str] = list()
    for row in range(len(df)):
        full_path = os.path.join(df.iloc[row]['path'], df.iloc[row]['name'])
        result.append(full_path)
    return result
