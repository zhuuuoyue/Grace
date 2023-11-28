# -*- coding: utf-8 -*-

import math
from enum import IntEnum, auto
from typing import Union, Tuple, Optional

import numpy as np

from shared import math as m

from .line_segment import LineSegment


class SpatialRelationship(IntEnum):

    UNKNOWN = auto()
    PARALLEL = auto()
    PERPENDICULAR = auto()


def is_close(a: Union[float, None], b: Union[float, None], tol: Optional[float] = None) -> bool:
    if a is None and b is None:
        return True
    if a is not None and b is not None:
        return m.is_close(a, b, tol)
    return False


def calculate_angle(first_line: LineSegment, second_line: LineSegment) -> Tuple[bool, float, str]:
    """计算两条直线段之间的夹角

    Args:
        first_line: 第一条直线段
        second_line: 第二条直线段

    Returns: 计算结果，三元组 [结果是否有效，角度，错误信息]
    """
    first_segment_length = first_line.start_point.distance(first_line.end_point)
    if is_close(first_segment_length, 0):
        return False, 0, '第一条线段长度为 0'
    second_segment = second_line.start_point.distance(second_line.end_point)
    if is_close(second_segment, 0):
        return False, 0, '第二条线段长度为 0'
    first_start_point = np.array([first_line.start_point.x, first_line.start_point.y])
    first_end_point = np.array([first_line.end_point.x, first_line.end_point.y])
    second_start_point = np.array([second_line.start_point.x, second_line.start_point.y])
    second_end_point = np.array([second_line.end_point.x, second_line.end_point.y])
    first_vector = first_start_point - first_end_point
    second_vector = second_start_point - second_end_point
    angle = math.atan2(np.linalg.det([first_vector, second_vector]), np.dot(first_vector, second_vector))
    angle = math.fabs(np.degrees(angle)) % 180
    if m.greater_than(angle, 90):
        angle = 180 - angle
    return True, angle, ''


def infer_spatial_relationship(angle: float, tolerance: float) -> SpatialRelationship:
    if m.is_close(angle, 90, tolerance):
        return SpatialRelationship.PERPENDICULAR
    elif m.is_zero(angle, tolerance):
        return SpatialRelationship.PARALLEL
    else:
        return SpatialRelationship.UNKNOWN
