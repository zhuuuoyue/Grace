# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Optional, Sequence, Union, List

from PySide6.QtCore import QObject, Slot, Signal, Property, Qt, QSignalBlocker
from PySide6.QtWidgets import (
    QApplication, QWidget, QDialog, QComboBox, QTableWidget, QTableWidgetItem, QPlainTextEdit,
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QClipboard

from command import ICommand
from tasks.create import TemplateData, EditTemplateTasks, extract_parameters, complete_template

from ui import DialogBase, WidgetViewModelBase, WidgetModelBase
from ui.utils import create_no_focus_tool_button, add_layout_children


class Parameter(object):

    def __init__(self, name: str, value: Optional[str] = None):
        self.name: str = name
        self.value: str = str() if value is None else value

    def __eq__(self, other):
        if not isinstance(other, Parameter):
            return False
        return self.name == other.name and self.value == other.value

    def __hash__(self):
        return self.name.__hash__()


class CreateUsingTemplateModel(WidgetModelBase):

    templates_changed = Signal(type(Sequence[TemplateData]))
    current_template_id_changed = Signal(int)
    parameters_changed = Signal(type(Sequence[Parameter]))
    parameter_value_changed = Signal(str, str)
    generated_content_changed = Signal(str)

    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)
        self.__templates: Sequence[TemplateData] = tuple()
        self.__current_template_id: int = 0
        self.__parameters: Sequence[Parameter] = list()
        self.__generated_content: str = str()

    def get_templates(self) -> Sequence[TemplateData]:
        return self.__templates

    def set_templates(self, value: Sequence[TemplateData]):
        if self.templates != value:
            self.__templates = value
            self.templates_changed.emit(self.templates)

    templates = Property(type(Sequence[TemplateData]), fget=get_templates, fset=set_templates, notify=templates_changed)

    def get_current_template_id(self) -> int:
        return self.__current_template_id

    def set_current_template_id(self, value: int):
        if self.current_template_id != value:
            self.__current_template_id = value
            self.current_template_id_changed.emit(self.current_template_id)

    current_template_id = Property(int, fget=get_current_template_id, fset=set_current_template_id,
                                   notify=current_template_id_changed)

    def get_parameters(self) -> Sequence[Parameter]:
        return self.__parameters

    def set_parameters(self, value: Sequence[Parameter]):
        if self.parameters != value:
            self.__parameters = value
            self.parameters_changed.emit(self.parameters)

    parameters = Property(type(Sequence[Parameter]), fget=get_parameters, fset=set_parameters,
                          notify=parameters_changed)

    def get_generated_content(self) -> str:
        return self.__generated_content

    def set_generated_content(self, value: str):
        if self.generated_content != value:
            self.__generated_content = value
            self.generated_content_changed.emit(self.generated_content)

    generated_content = Property(str, fget=get_generated_content, fset=set_generated_content,
                                 notify=generated_content_changed)

    def initialize(self):
        self.templates_changed.connect(self.__on_templates_changed)
        self.current_template_id_changed.connect(self.__on_current_template_id_changed)
        self.parameters_changed.connect(self.__on_parameters_changed)
        self.parameter_value_changed.connect(self.__on_parameter_value_changed)
        self.update()

    def update(self):
        self.templates = tuple()
        self.templates = EditTemplateTasks.get_templates()

    def get_current_template(self) -> Union[TemplateData, None]:
        for template in self.templates:
            if self.current_template_id == template.id:
                return template

    def set_parameter_value(self, name: str, value: str):
        for parameter in self.parameters:
            if parameter.name == name:
                parameter.value = value
                self.parameter_value_changed.emit(parameter.name, parameter.value)

    def reset_parameters(self):
        parameters = deepcopy(self.parameters)
        for parameter in parameters:
            parameter.value = str()
        self.parameters = parameters

    @Slot(type(Sequence[TemplateData]))
    def __on_templates_changed(self, templates: Sequence[TemplateData]):
        self.current_template_id = 0 if len(templates) == 0 else templates[0].id

    @Slot(int)
    def __on_current_template_id_changed(self, current_template_id: int):
        current_template = self.get_current_template()
        if current_template is not None:
            parameters = extract_parameters(current_template.content)
            self.parameters = [Parameter(parameter) for parameter in parameters]

    def __regenerate_content(self):
        current_template = self.get_current_template()
        if current_template is None:
            return

        parameter_dict = dict()
        for parameter in self.parameters:
            parameter_dict[parameter.name] = parameter.value

        self.generated_content = complete_template(current_template.content, parameter_dict)

    @Slot(type(Sequence[Parameter]))
    def __on_parameters_changed(self, parameters: Sequence[Parameter]):
        self.__regenerate_content()

    @Slot(str, str)
    def __on_parameter_value_changed(self, name: str, value: str):
        self.__regenerate_content()


class CreateUsingTemplateViewModel(WidgetViewModelBase):

    templates_changed = Signal(type(List[str]))
    current_template_index_changed = Signal(int)
    parameters_changed = Signal(type(List[Parameter]))
    parameter_value_changed = Signal(int, str)
    generated_content_changed = Signal(str)

    def __init__(self, parent: Optional[QObject]):
        super().__init__(parent)
        self.__model = CreateUsingTemplateModel(self)
        self.__templates: List[str] = list()
        self.__current_template_index: int = -1
        self.__parameters: List[Parameter] = list()
        self.__generated_content: str = str()

    @property
    def model(self) -> CreateUsingTemplateModel:
        return self.__model

    def get_templates(self) -> List[str]:
        return self.__templates

    def set_templates(self, value: List[str]):
        if self.templates != value:
            self.__templates = value
            self.templates_changed.emit(self.templates)

    templates = Property(type(List[str]), fget=get_templates, fset=set_templates, notify=templates_changed)

    def get_current_template_index(self) -> int:
        return self.__current_template_index

    def set_current_template_index(self, value: int):
        if self.current_template_index != value:
            self.__current_template_index = value
            self.current_template_index_changed.emit(self.current_template_index)

    current_template_index = Property(int, fget=get_current_template_index, fset=set_current_template_index,
                                      notify=current_template_index_changed)

    def get_parameters(self) -> List[Parameter]:
        return self.__parameters

    def set_parameters(self, value: List[Parameter]):
        if self.parameters != value:
            self.__parameters = value
            self.parameters_changed.emit(self.parameters)

    parameters = Property(type(List[Parameter]), fget=get_parameters, fset=set_parameters, notify=parameters_changed)

    def get_generated_content(self) -> str:
        return self.__generated_content

    def set_generated_content(self, value: str):
        if self.generated_content != value:
            self.__generated_content = value
            self.generated_content_changed.emit(self.generated_content)

    generated_content = Property(str, fget=get_generated_content, fset=set_generated_content,
                                 notify=generated_content_changed)

    def initialize(self):
        self.model.templates_changed.connect(self.__on_model_templates_changed)
        self.model.current_template_id_changed.connect(self.__on_model_current_template_id_changed)
        self.model.parameters_changed.connect(self.__on_model_parameters_changed)
        self.model.parameter_value_changed.connect(self.__on_model_parameter_value_changed)
        self.model.generated_content_changed.connect(self.__on_model_generated_content_changed)
        self.model.initialize()

    def update(self):
        self.model.update()

    def set_parameter_value(self, index: int, value: str):
        name = self.model.parameters[index].name
        self.model.set_parameter_value(name, value)

    def reset_parameters(self):
        self.model.reset_parameters()

    def switch_template(self, index: int):
        template_id = self.model.templates[index].id
        self.model.set_current_template_id(template_id)

    @Slot(type(Sequence[TemplateData]))
    def __on_model_templates_changed(self, templates: Sequence[TemplateData]):
        self.templates = [template.name for template in templates]

    @Slot(int)
    def __on_model_current_template_id_changed(self, current_template_id: int):
        for index, template in enumerate(self.model.templates):
            if template.id == current_template_id:
                self.current_template_index = index
                break

    @Slot(str, str)
    def __on_model_parameter_value_changed(self, name: str, value: str):
        for index, parameter in enumerate(self.parameters):
            if parameter.name == name:
                parameter.value = value
                self.parameter_value_changed.emit(index, value)

    @Slot(type(Sequence[Parameter]))
    def __on_model_parameters_changed(self, parameters: Sequence[Parameter]):
        self.parameters = [deepcopy(parameter) for parameter in parameters]

    @Slot(str)
    def __on_model_generated_content_changed(self, generated_content: str):
        self.generated_content = generated_content


class CreateUsingTemplateView(object):

    def __init__(self, dialog: QDialog):
        dialog.setWindowTitle('Create Using Template')
        dialog.setSizeGripEnabled(True)

        self.preview = QPlainTextEdit()
        self.preview.setStyleSheet(
            '''
            font-family: 'consolas';
            font-size: 14px;
            '''
        )

        self.template_selector = QComboBox()

        self.parameter_table = QTableWidget()
        self.parameter_table.setColumnCount(2)
        self.parameter_table.setHorizontalHeaderLabels(['Parameter', 'Value'])

        self.button_copy = create_no_focus_tool_button('copy', 'Copy generated content')
        self.button_clean = create_no_focus_tool_button('clean', 'Clean parameter values')
        self.button_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(8)
        add_layout_children(self.button_layout, [self.button_copy, self.button_clean, self.button_spacer])

        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(4)
        add_layout_children(self.right_layout, [self.template_selector, self.parameter_table, self.button_layout])

        self.right_widget = QWidget()
        self.right_widget.setFixedWidth(280)
        self.right_widget.setLayout(self.right_layout)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(8)
        add_layout_children(self.layout, [self.preview, self.right_widget])
        dialog.setLayout(self.layout)


class CreateUsingTemplateDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(object_name='a6de0969-8678-46e8-8eb2-4eb1fe551d16', parent=parent)
        self.ui = CreateUsingTemplateView(self)
        self.vm = CreateUsingTemplateViewModel(self)

    def initialize(self):
        self.vm.templates_changed.connect(self.__on_vm_templates_changed)
        self.vm.current_template_index_changed.connect(self.ui.template_selector.setCurrentIndex)
        self.vm.parameters_changed.connect(self.__on_vm_parameters_changed)
        self.vm.generated_content_changed.connect(self.ui.preview.setPlainText)
        self.ui.parameter_table.cellChanged.connect(self.__on_ui_parameter_table_cell_changed)
        self.ui.button_copy.clicked.connect(self.__on_ui_button_copy_clicked)
        self.ui.button_clean.clicked.connect(self.__on_ui_button_clean_clicked)
        self.ui.template_selector.currentIndexChanged.connect(self.vm.switch_template)
        self.vm.initialize()

    @Slot(type(List[str]))
    def __on_vm_templates_changed(self, templates: List[str]):
        self.ui.template_selector.clear()
        self.ui.template_selector.addItems(templates)

    @Slot(type(List[Parameter]))
    def __on_vm_parameters_changed(self, parameters: List[Parameter]):
        table = self.ui.parameter_table
        signal_blocker = QSignalBlocker(table)

        table.setRowCount(len(parameters))
        for row_index, parameter in enumerate(parameters):
            parameter_key_item = QTableWidgetItem()
            parameter_key_item.setText(parameter.name)
            parameter_key_item.setFlags(parameter_key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(row_index, 0, parameter_key_item)

            parameter_value_item = QTableWidgetItem()
            parameter_value_item.setText(parameter.value)
            table.setItem(row_index, 1, parameter_value_item)

        signal_blocker.unblock()

    @Slot(int, str)
    def __on_vm_parameter_value_changed(self, index: int, value: str):
        table = self.ui.parameter_table
        signal_blocker = QSignalBlocker(table)
        if table.item(index, 1).text() != value:
            table.item(index, 1).setText(value)
        signal_blocker.unblock()

    @Slot(int, int)
    def __on_ui_parameter_table_cell_changed(self, row: int, col: int):
        if col != 1:
            return
        table = self.ui.parameter_table
        value = table.item(row, 1).text()
        self.vm.set_parameter_value(row, value)

    @Slot()
    def __on_ui_button_clean_clicked(self):
        self.vm.reset_parameters()

    @Slot()
    def __on_ui_button_copy_clicked(self):
        content = self.vm.model.generated_content
        clipboard = QApplication.clipboard()
        clipboard.setText(content)


class CreateUsingTemplateCommand(ICommand):

    def exec(self, *args, **kwargs):
        dialog = CreateUsingTemplateDialog()
        dialog.initialize()
        dialog.exec()
