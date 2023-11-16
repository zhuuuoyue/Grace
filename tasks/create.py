# -*- coding: utf-8 -*-

from typing import Set, Sequence, Union


class TemplateData(object):

    def __init__(self):
        self.name: str = str()
        self.content: str = str()

    def __str__(self):
        return f'name: \'{self.name}\', content: \'{self.content}\''


class EditTemplateTasks(object):

    def add_template(self, template: TemplateData) -> bool:
        pass

    def add_templates(self, templates: Sequence[TemplateData]) -> bool:
        pass

    def delete_template(self, template_name: str) -> bool:
        pass

    def update_template(self, template: TemplateData) -> bool:
        pass

    def get_template_names(self) -> Set[str]:
        pass

    def get_template_content_using_name(self, name: str) -> Union[str, None]:
        pass
