# -*- coding: utf-8 -*-

from shapely import Point

from shared import math as m


class LineSegment(object):

    def __init__(self, start_point: Point, end_point: Point):
        self.start_point: Point = start_point
        self.end_point: Point = end_point

    def __str__(self):
        return f'LineSegment({self.start_point} -> {self.end_point})'

    def __eq__(self, other):
        if not isinstance(other, LineSegment):
            return False
        start_point_distance = self.start_point.distance(other.start_point)
        end_point_distance = self.end_point.distance(other.end_point)
        return m.is_zero(start_point_distance) and m.is_zero(end_point_distance)
