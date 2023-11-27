# -*- coding: utf-8 -*-

from typing import Tuple, List, Union

from shapely import Point, MultiPoint
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import Line2D

from shared import math as m

from .line_segment import LineSegment

BoundingBox = Tuple[float, float, float, float]


class LineSegmentVisualizer(FigureCanvasQTAgg):

    def __init__(self):
        figure = Figure()
        super().__init__(figure)
        self.__axes = figure.add_axes((0.09, 0.09, 0.9, 0.9))
        self.__axes.set_aspect('equal')
        self.__axes.set_adjustable('datalim')
        self.__first_line_segment_data: Union[LineSegment, None] = None
        self.__first_line_segment_curve: Union[Line2D, None] = None
        self.__second_line_segment_data: Union[LineSegment, None] = None
        self.__second_line_segment_curve: Union[Line2D, None] = None

    @staticmethod
    def create_xs_and_ys(line: LineSegment) -> Tuple[List[float], List[float]]:
        return [line.start_point.x, line.end_point.x], [line.start_point.y, line.end_point.y]

    def get_bounding_box(self) -> Union[BoundingBox, None]:
        points: List[Point] = list()
        if self.__first_line_segment_data is not None:
            points.append(self.__first_line_segment_data.start_point)
            points.append(self.__first_line_segment_data.end_point)
        if self.__second_line_segment_data is not None:
            points.append(self.__second_line_segment_data.start_point)
            points.append(self.__second_line_segment_data.end_point)
        return None if len(points) == 0 else MultiPoint(points).bounds

    def update_figure(self):
        x_min_limit = 0
        x_max_limit = 1
        y_min_limit = 0
        y_max_limit = 1
        box = self.get_bounding_box()
        if box is not None:
            delta_x = box[2] - box[0]
            delta_y = box[3] - box[1]
            radius = max(delta_x, delta_y) / 2.0 * 1.1
            if m.is_zero(radius):
                radius = 1

            center_x = (box[0] + box[2]) / 2.0
            x_min_limit = center_x - radius
            x_max_limit = center_x + radius

            center_y = (box[1] + box[3]) / 2.0
            y_min_limit = center_y - radius
            y_max_limit = center_y + radius

        self.__axes.set_xlim(x_min_limit, x_max_limit)
        self.__axes.set_ylim(y_min_limit, y_max_limit)
        self.draw()

    def update_first_line_segment(self, line_segment: LineSegment):
        self.remove_first_line_segment()
        self.__first_line_segment_data = line_segment
        lines = self.__axes.plot(*self.create_xs_and_ys(line_segment), color='blue')
        self.__first_line_segment_curve = lines[0]
        self.update_figure()

    def update_second_line_segment(self, line_segment: LineSegment):
        self.remove_second_line_segment()
        self.__second_line_segment_data = line_segment
        lines = self.__axes.plot(*self.create_xs_and_ys(line_segment), color='green')
        self.__second_line_segment_curve = lines[0]
        self.update_figure()

    def remove_first_line_segment(self):
        if self.__first_line_segment_curve is not None:
            self.__first_line_segment_curve.remove()
            self.__first_line_segment_curve = None
            self.__first_line_segment_data = None
            self.update_figure()

    def remove_second_line_segment(self):
        if self.__second_line_segment_curve is not None:
            self.__second_line_segment_curve.remove()
            self.__second_line_segment_curve = None
            self.__second_line_segment_data = None
            self.update_figure()
