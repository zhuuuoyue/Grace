# -*- coding: utf-8 -*-

import os

import context


def get_image_path(image_name: str) -> str:
    return os.path.join(context.get_context().image_directory, f'{image_name}.png')
