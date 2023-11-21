# -*- coding: utf-8 -*-

import os
import shutil
from typing import Union

from extensions.gna.concept import Environment


class SwitchEnvironmentTask(object):

    def __init__(self):
        self.__path_to_software_package: Union[str, None] = None
        self.__target_environment: Environment = Environment.QA

    def set_software_package_directory(self, path_to_software_package: str):
        self.__path_to_software_package = path_to_software_package

    def set_target_environment(self, env: Environment):
        self.__target_environment = env

    def run(self):
        dst_dir = self.__path_to_software_package
        mapping = {
            Environment.A: 'a',
            Environment.B: 'b',
            Environment.C: 'c',
            Environment.QA: 'qa',
            Environment.QA_STG: 'qastg'
        }
        src_dir = os.path.join(dst_dir, 'SwitchEnvironment', mapping[self.__target_environment])
        children = os.listdir(src_dir)
        for child in children:
            full_path = os.path.join(src_dir, child)
            if os.path.isdir(full_path):
                self.replace_directory(src_dir, dst_dir, full_path)
            elif os.path.isfile(full_path):
                self.replace_file(src_dir, dst_dir, full_path)

    @staticmethod
    def replace_directory(src_dir: str, dst_dir: str, dir_path: str):
        src_dir_path = dir_path
        dst_dir_path = os.path.join(dst_dir, os.path.relpath(dir_path, src_dir))
        if not os.path.isdir(dst_dir_path):
            os.mkdir(dst_dir_path)
        to_copy_list = os.listdir(src_dir_path)
        for to_copy_item in to_copy_list:
            full_path = os.path.join(src_dir_path, to_copy_item)
            if os.path.isdir(full_path):
                SwitchEnvironmentTask.replace_directory(src_dir, dst_dir, full_path)
            elif os.path.isfile(full_path):
                SwitchEnvironmentTask.replace_file(src_dir, dst_dir, full_path)

    @staticmethod
    def replace_file(src_dir: str, dst_dir: str, file_path: str):
        src_file_path = file_path
        if not os.path.isfile(src_file_path):
            return

        dst_file_path = os.path.join(dst_dir, os.path.relpath(file_path, src_dir))
        if os.path.isfile(dst_file_path):
            os.remove(dst_file_path)
        shutil.copyfile(src_file_path, dst_file_path)
