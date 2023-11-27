# -*- coding: utf-8 -*-

import math
from enum import IntEnum, auto
from typing import Optional, Union, Tuple, List

import numpy as np
from shapely import Point, MultiPoint
from PySide6.QtCore import Qt, Slot, Signal, Property, QObject
from PySide6.QtWidgets import QDialog, QWidget, QLineEdit, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QCloseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import Line2D

from shared import math as m
from command import ICommand
from ui import WidgetModelBase, WidgetViewModelBase, DialogBase
from ui.utils import create_row_title, create_row_layout, create_column_layout, add_layout_children
from ui.cache import get_ui_cache


class Line(object):

    def __init__(self, start_point: Point, end_point: Point):
        self.start_point: Point = start_point
        self.end_point: Point = end_point

    def __str__(self):
        return f'Line({self.start_point} -> {self.end_point})'

    def __eq__(self, other):
        if not isinstance(other, Line):
            return False
        start_point_distance = self.start_point.distance(other.start_point)
        end_point_distance = self.end_point.distance(other.end_point)
        return m.is_zero(start_point_distance) and m.is_zero(end_point_distance)


BBox = Tuple[float, float, float, float]


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


def calculate_angle(first_line: Line, second_line: Line) -> Tuple[bool, float, str]:
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


class SpatialRelationshipOfTwoLinesModel(WidgetModelBase):

    first_line_changed = Signal(type(Union[Line, None]))
    second_line_changed = Signal(type(Union[Line, None]))
    angle_changed = Signal(type(Union[float, None]))
    tolerance_changed = Signal(type(Union[float, None]))
    conclusion_changed = Signal(type(SpatialRelationship))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__first_line: Union[Line, None] = None
        self.__second_line: Union[Line, None] = None
        self.__angle: Union[float, None] = None
        self.__tolerance: Union[float, None] = None
        self.__conclusion: SpatialRelationship = SpatialRelationship.UNKNOWN

    def get_first_line(self) -> Union[Line, None]:
        return self.__first_line

    def set_first_line(self, value: Union[Line, None]):
        if self.first_line != value:
            self.__first_line = value
            self.first_line_changed.emit(self.first_line)

    first_line = Property(type(Union[Line, None]), fget=get_first_line, fset=set_first_line, notify=first_line_changed)

    def get_second_line(self) -> Union[Line, None]:
        return self.__second_line

    def set_second_line(self, value: Union[Line, None]):
        if self.second_line != value:
            self.__second_line = value
            self.second_line_changed.emit(self.second_line)

    second_line = Property(type(Union[Line, None]), fget=get_second_line, fset=set_second_line,
                           notify=second_line_changed)

    def get_angle(self) -> Union[float, None]:
        return self.__angle

    def set_angle(self, value: Union[float, None]):
        if not is_close(self.angle, value):
            self.__angle = value
            self.angle_changed.emit(self.angle)

    angle = Property(type(Union[float, None]), fget=get_angle, fset=set_angle, notify=angle_changed)

    def get_tolerance(self) -> Union[float, None]:
        return self.__tolerance

    def set_tolerance(self, value: Union[float, None]):
        if not is_close(self.tolerance, value):
            self.__tolerance = value
            self.tolerance_changed.emit(self.tolerance)

    tolerance = Property(type(Union[float, None]), fget=get_tolerance, fset=set_tolerance, notify=tolerance_changed)

    def get_conclusion(self) -> SpatialRelationship:
        return self.__conclusion

    def set_conclusion(self, value: SpatialRelationship):
        if self.conclusion != value:
            self.__conclusion = value
            self.conclusion_changed.emit(self.conclusion)

    conclusion = Property(type(SpatialRelationship), fget=get_conclusion, fset=set_conclusion,
                          notify=conclusion_changed)

    def initialize(self):
        # connect
        self.first_line_changed.connect(self.__on_first_line_changed)
        self.second_line_changed.connect(self.__on_second_line_changed)
        self.angle_changed.connect(self.__on_angle_changed)
        self.tolerance_changed.connect(self.__on_tolerance_changed)
        # update
        self.update()

    def update(self):
        self.tolerance = np.degrees(m.FLOAT_TOLERANCE)

    def update_angle(self):
        if self.first_line is None or self.second_line is None:
            self.angle = None
        else:
            ok, angle, error = calculate_angle(self.get_first_line(), self.get_second_line())
            self.angle = angle if ok else None

    def update_conclusion(self):
        if self.angle is None:
            self.conclusion = SpatialRelationship.UNKNOWN
        else:
            self.conclusion = infer_spatial_relationship(self.angle, self.tolerance)

    @Slot(type(Union[Line, None]))
    def __on_first_line_changed(self, first_line: Union[Line, None]):
        self.update_angle()

    @Slot(type(Union[Line, None]))
    def __on_second_line_changed(self, second_line: Union[Line, None]):
        self.update_angle()

    @Slot(type(Union[float, None]))
    def __on_angle_changed(self, angle: Union[float, None]):
        self.update_conclusion()

    @Slot(type(Union[float, None]))
    def __on_tolerance_changed(self, tolerance: Union[float, None]):
        self.update_conclusion()


class SpatialRelationshipOfTwoLinesViewModel(WidgetViewModelBase):

    angle_text_changed = Signal(type(str))
    conclusion_text_changed = Signal(type(str))

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.__model = SpatialRelationshipOfTwoLinesModel(self)
        self.__angle_text: str = str()
        self.__conclusion_text: str = str()

    @property
    def model(self) -> SpatialRelationshipOfTwoLinesModel:
        return self.__model

    def get_angle_text(self) -> str:
        return self.__angle_text

    def set_angle_text(self, value: str):
        if self.angle_text != value:
            self.__angle_text = value
            self.angle_text_changed.emit(self.angle_text)

    angle_text = Property(type(str), fget=get_angle_text, fset=set_angle_text, notify=angle_text_changed)

    def get_conclusion_text(self) -> str:
        return self.__conclusion_text

    def set_conclusion_text(self, value: str):
        if self.conclusion_text != value:
            self.__conclusion_text = value
            self.conclusion_text_changed.emit(self.conclusion_text)

    conclusion_text = Property(type(str), fget=get_conclusion_text, fset=set_conclusion_text,
                               notify=conclusion_text_changed)

    def initialize(self):
        self.model.angle_changed.connect(self.__on_model_angle_changed)
        self.model.conclusion_changed.connect(self.__on_model_conclusion_changed)
        self.model.initialize()

    def update(self):
        self.model.update()

    @Slot(type(Union[float, None]))
    def __on_model_angle_changed(self, angle: Union[float, None]):
        self.angle_text = str() if angle is None else f'{angle} degree, {np.radians(angle)} radian'

    @Slot(type(SpatialRelationship))
    def __on_model_conclusion_changed(self, conclusion: SpatialRelationship):
        self.conclusion_text = {
            SpatialRelationship.UNKNOWN: '',
            SpatialRelationship.PARALLEL: 'Parallel',
            SpatialRelationship.PERPENDICULAR: 'Perpendicular',
        }[conclusion]


class DoubleInput(QLineEdit):

    value_changed = Signal(type(Union[float, None]))

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.editingFinished.connect(self.__on_editing_finished)
        self.__value: Union[float, None] = None

    def get_value(self) -> Union[float, None]:
        return self.__value

    def set_value(self, value: Union[float, None]):
        if self.value != value:
            self.__value = value
            self.update_view()
            self.value_changed.emit(self.value)

    value = Property(type(Union[float, None]), fget=get_value, fset=set_value, notify=value_changed)

    def update_view(self):
        current_value = self.get_value_from_input(self.text())
        if not is_close(current_value, self.value, m.FLOAT_TOLERANCE):
            if self.value is None:
                self.setText('')
            else:
                self.setText(f'{self.value:.7f}')

    @Slot()
    def __on_editing_finished(self):
        self.value = self.get_value_from_input(self.text())

    @staticmethod
    def get_value_from_input(text: str) -> Union[float, None]:
        try:
            value = float(text)
            return value
        except ValueError:
            return None


def create_symbol_label(text: str) -> QLabel:
    label = QLabel()
    label.setFixedWidth(8)
    label.setText(text)
    return label


class PointInput(QWidget):

    point_changed = Signal(type(Union[Point, None]))

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        css = '''font-family: 'consolas';
        font-size: 13px;
        border: none;
        '''
        self.__left_parenthesis = create_symbol_label('(')
        self.__x_input = DoubleInput()
        self.__x_input.setStyleSheet(css)
        self.__comma = create_symbol_label(',')
        self.__y_input = DoubleInput()
        self.__y_input.setStyleSheet(css)
        self.__right_parenthesis = create_symbol_label(')')
        self.__layout = QHBoxLayout()
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        add_layout_children(
            self.__layout,
            [self.__left_parenthesis, self.__x_input, self.__comma, self.__y_input, self.__right_parenthesis]
        )
        self.setLayout(self.__layout)

        self.__x_input.value_changed.connect(self.__on_dimension_value_changed)
        self.__y_input.value_changed.connect(self.__on_dimension_value_changed)

    def get_point(self) -> Union[Point, None]:
        x = self.__x_input.get_value()
        y = self.__y_input.get_value()
        if x is None or y is None:
            return None
        else:
            return Point(x, y)

    @Slot(type(Union[float, None]))
    def __on_dimension_value_changed(self, value: Union[float, None]):
        self.point_changed.emit(self.get_point())


class LineInput(QWidget):

    line_changed = Signal(type(Union[Line, None]))

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.__start_point_input = PointInput()
        self.__separator = create_symbol_label('-')
        self.__end_point_input = PointInput()
        self.__layout = QHBoxLayout()
        self.__layout.setSpacing(0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        add_layout_children(self.__layout, [self.__start_point_input, self.__separator, self.__end_point_input])
        self.setLayout(self.__layout)

        self.__start_point_input.point_changed.connect(self.__on_endpoint_changed)
        self.__end_point_input.point_changed.connect(self.__on_endpoint_changed)

    @Slot(type(Union[Point, None]))
    def __on_endpoint_changed(self, endpoint: Union[Point, None]):
        start_point = self.__start_point_input.get_point()
        end_point = self.__end_point_input.get_point()
        if start_point is None or end_point is None:
            self.line_changed.emit(None)
        else:
            self.line_changed.emit(Line(start_point, end_point))


class Visualizer(FigureCanvasQTAgg):

    def __init__(self):
        figure = Figure()
        super().__init__(figure)
        self.__axes = figure.add_axes((0.09, 0.09, 0.9, 0.9))
        self.__axes.set_aspect('equal')
        self.__axes.set_adjustable('datalim')
        self.__first_line_data: Union[Line, None] = None
        self.__first_line_curve: Union[Line2D, None] = None
        self.__second_line_data: Union[Line, None] = None
        self.__second_line_curve: Union[Line2D, None] = None

    @staticmethod
    def create_xs_and_ys(line: Line) -> Tuple[List[float], List[float]]:
        return [line.start_point.x, line.end_point.x], [line.start_point.y, line.end_point.y]

    def get_bounding_box(self) -> Union[BBox, None]:
        points: List[Point] = list()
        if self.__first_line_data is not None:
            points.append(self.__first_line_data.start_point)
            points.append(self.__first_line_data.end_point)
        if self.__second_line_data is not None:
            points.append(self.__second_line_data.start_point)
            points.append(self.__second_line_data.end_point)
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

    def update_first_line(self, line: Line):
        self.remove_first_line()
        self.__first_line_data = line
        lines = self.__axes.plot(*self.create_xs_and_ys(line), color='blue')
        self.__first_line_curve = lines[0]
        self.update_figure()

    def update_second_line(self, line: Line):
        self.remove_second_line()
        self.__second_line_data = line
        lines = self.__axes.plot(*self.create_xs_and_ys(line), color='green')
        self.__second_line_curve = lines[0]
        self.update_figure()

    def remove_first_line(self):
        if self.__first_line_curve is not None:
            self.__first_line_curve.remove()
            self.__first_line_curve = None
            self.__first_line_data = None
            self.update_figure()

    def remove_second_line(self):
        if self.__second_line_curve is not None:
            self.__second_line_curve.remove()
            self.__second_line_curve = None
            self.__second_line_data = None
            self.update_figure()


class SpatialRelationshipOfTwoLinesView(object):

    def __init__(self, dialog: QDialog):
        dialog.setWindowTitle(r'Infer Spatial Relationship of Two Line Segments')
        dialog.setFixedSize(616, 760)

        self.visualizer = Visualizer()
        self.visualizer.setFixedSize(600, 600)

        self.first_line_title = create_row_title(r'First Line')
        self.first_line_input = LineInput()
        self.first_line_layout = create_row_layout(title=self.first_line_title, widget=self.first_line_input)

        self.second_line_title = create_row_title(r'Second Line')
        self.second_line_input = LineInput()
        self.second_line_layout = create_row_layout(title=self.second_line_title, widget=self.second_line_input)

        self.angle_title = create_row_title(r'Angle')
        self.angle = QLineEdit()
        self.angle.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.angle.setStyleSheet(
            '''
            font-family: 'Consolas';
            font-size: 14px;
            '''
        )
        self.angle_layout = create_row_layout(title=self.angle_title, widget=self.angle)

        self.tolerance_title = create_row_title(r'Tolerance')
        self.degree_input, self.degree_unit = self.create_tolerance_input('degree')
        self.tolerance_spacer = QSpacerItem(24, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.radian_input, self.radian_unit = self.create_tolerance_input('radian')
        self.tolerance_layout = create_row_layout(
            title=self.tolerance_title,
            widgets=[self.degree_input, self.degree_unit, self.tolerance_spacer, self.radian_input, self.radian_unit],
            append_spacer=True
        )

        self.conclusion_title = create_row_title(r'Conclusion')
        self.conclusion = QLineEdit()
        self.conclusion.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.conclusion_layout = create_row_layout(title=self.conclusion_title, widget=self.conclusion)

        self.layout = create_column_layout(
            children=[
                self.visualizer,
                self.first_line_layout,
                self.second_line_layout,
                self.angle_layout,
                self.tolerance_layout,
                self.conclusion_layout
            ]
        )
        self.layout.setContentsMargins(8, 8, 8, 8)
        dialog.setLayout(self.layout)

    @staticmethod
    def create_tolerance_input(unit: str) -> Tuple[DoubleInput, QLabel]:
        value_input = DoubleInput()
        value_input.setFixedWidth(96)
        value_input.setStyleSheet(
            '''
            font-family: 'Consolas';
            font-size: 14px;
            '''
        )
        unit_label = QLabel(unit)
        unit_label.setFixedWidth(48)
        unit_label.setStyleSheet(
            '''
            margin-left: 4px;
            font-family: 'Consolas';
            font-size: 13px;
            '''
        )
        return value_input, unit_label


class SpatialRelationshipOfTwoLinesDialog(DialogBase):

    __instance__ = None

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(object_name='6a69811c-e16c-43b9-b14d-7a10df891fd9', parent=parent)
        self.ui = SpatialRelationshipOfTwoLinesView(self)
        self.vm = SpatialRelationshipOfTwoLinesViewModel(self)

    @staticmethod
    def get_dialog():
        if SpatialRelationshipOfTwoLinesDialog.__instance__ is None:
            dialog = SpatialRelationshipOfTwoLinesDialog()
            dialog.setWindowModality(Qt.WindowModality.NonModal)
            dialog.initialize()
            SpatialRelationshipOfTwoLinesDialog.__instance__ = dialog
        return SpatialRelationshipOfTwoLinesDialog.__instance__

    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        SpatialRelationshipOfTwoLinesDialog.__instance__ = None
        get_ui_cache().save()

    def initialize(self):
        # signals from view
        self.ui.first_line_input.line_changed.connect(self.__on_ui_first_line_changed)
        self.ui.second_line_input.line_changed.connect(self.__on_ui_second_line_changed)
        self.ui.degree_input.value_changed.connect(self.__on_ui_tolerance_degree_value_changed)
        self.ui.radian_input.value_changed.connect(self.__on_ui_tolerance_radian_value_changed)

        # signals from view model
        self.vm.angle_text_changed.connect(self.ui.angle.setText)
        self.vm.conclusion_text_changed.connect(self.ui.conclusion.setText)

        # signals from model
        self.vm.model.tolerance_changed.connect(self.__on_model_tolerance_degree_value_changed)
        self.vm.model.tolerance_changed.connect(self.__on_model_tolerance_radian_value_changed)

        # initialize
        self.vm.initialize()

    @Slot(type(Union[Line, None]))
    def __on_ui_first_line_changed(self, line: Union[Line, None]):
        self.vm.model.first_line = line
        if line is None:
            self.ui.visualizer.remove_first_line()
        else:
            self.ui.visualizer.update_first_line(line)

    @Slot(type(Union[Line, None]))
    def __on_ui_second_line_changed(self, line: Union[Line, None]):
        self.vm.model.second_line = line
        if line is None:
            self.ui.visualizer.remove_second_line()
        else:
            self.ui.visualizer.update_second_line(line)

    @Slot(type(Union[float, None]))
    def __on_ui_tolerance_degree_value_changed(self, value: Union[float, None]):
        self.vm.model.tolerance = value

    @Slot(type(Union[float, None]))
    def __on_ui_tolerance_radian_value_changed(self, value: Union[float, None]):
        self.vm.model.tolerance = None if value is None else np.degrees(value)

    @Slot(type(Union[float, None]))
    def __on_model_tolerance_degree_value_changed(self, value: Union[float, None]):
        self.ui.degree_input.set_value(value)

    @Slot(type(Union[float, None]))
    def __on_model_tolerance_radian_value_changed(self, value: Union[float, None]):
        if value is None:
            self.ui.radian_input.set_value(None)
        else:
            self.ui.radian_input.set_value(np.radians(value))


class SpatialRelationshipOfTwoLinesCommand(ICommand):

    def exec(self, *args, **kwargs):
        dialog = SpatialRelationshipOfTwoLinesDialog.get_dialog()
        dialog.show()
