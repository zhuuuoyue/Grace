# -*- coding: utf-8 -*-

from command import register_command
from shared.context import Context
from app import ActionData, MainWindow

from .CleanLogFiles import CleanLogFilesCommand
from .switch_environment import SwitchEnvironmentCommand
from .infer_spatial_relationship import InferSpatialRelationshipCommand


def initialize(ctx: Context):
    register_command('cmd_clean_log_files', CleanLogFilesCommand())
    register_command('cmd_switch_environment', SwitchEnvironmentCommand())
    register_command('cmd_infer_spatial_relationship', InferSpatialRelationshipCommand())

    win = ctx.main_window
    menu = 'GNA'
    if isinstance(win, MainWindow):
        win.add_action(menu, ActionData(command_id='cmd_clean_log_files',
                                        title='Clean Log Files',
                                        icon='clean',
                                        tooltip='Clean log files under architecture and structure software package'))
        win.add_action(menu, ActionData(command_id='cmd_switch_environment',
                                        title='Switch Environment',
                                        icon='chain',
                                        tooltip='Switch runtime environment'))
        win.add_action(menu, ActionData(command_id='cmd_infer_spatial_relationship',
                                        title='Infer Spatial Relationship',
                                        icon='cat-48',
                                        tooltip='Infer spatial relationship of two given line segments'))
