# -*- coding: utf-8 -*-

class TemplateData(object):

    def __init__(self):
        self.name: str = str()
        self.content: str = str()

    def __str__(self):
        return f'name: \'{self.name}\', content: \'{self.content}\''
