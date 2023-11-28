# -*- coding: utf-8 -*-

from typing import Optional


FLOAT_TOLERANCE: float = 0.0000001


def is_close(a: float, b: float, tolerance: Optional[float] = None) -> bool:
    tol = tolerance if tolerance is not None else FLOAT_TOLERANCE
    return abs(a - b) < tol


def greater_than(a: float, b: float, tolerance: Optional[float] = None) -> bool:
    return False if is_close(a, b, tolerance) else (a > b)


def less_than(a: float, b: float, tolerance: Optional[float] = None) -> bool:
    return False if is_close(a, b, tolerance) else (a < b)


def greater_than_or_is_close(a: float, b: float, tolerance: Optional[float]) -> bool:
    return True if is_close(a, b, tolerance) else (a > b)


def less_than_or_is_close(a: float, b: float, tolerance: Optional[float]) -> bool:
    return True if is_close(a, b, tolerance) else (a < b)


def is_zero(a: float, tolerance: Optional[float] = None) -> bool:
    return is_close(a, 0, tolerance)
