# -*- coding: utf-8 -*-

from typing import Optional

from .Identifiable import Identifiable


class DocumentData(Identifiable):

    def __init__(self, relative_path: Optional[str] = None, encoding_id: Optional[int] = None,
                 template_id: Optional[int] = None, document_id: Optional[int] = None):
        super().__init__(document_id)
        self.relative_path: str = str() if relative_path is None else relative_path
        self.encoding_id: int = 0 if encoding_id is None else encoding_id
        self.template_id: int = 0 if template_id is None else template_id
