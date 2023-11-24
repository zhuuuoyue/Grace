# -*- coding: utf-8 -*-

from command import register_command
from shared.context import Context
from app import ActionData, MainWindow

from .CleanLogFiles import CleanLogFilesCommand
from .switch_environment import SwitchEnvironmentCommand
from .spatial_relationship_of_two_lines import SpatialRelationshipOfTwoLinesCommand


def initialize(ctx: Context):
    register_command('cmd_clean_log_files', CleanLogFilesCommand())
    register_command('cmd_switch_environment', SwitchEnvironmentCommand())
    register_command('cmd_spatial_relationship_of_two_lines', SpatialRelationshipOfTwoLinesCommand())

    win = ctx.main_window
    menu = 'GNA'
    if isinstance(win, MainWindow):
        win.add_action(menu, ActionData(command_id='cmd_clean_log_files', title='Clean Log Files', icon='clean',
                                        tooltip='Clean log files under architecture and structure software package'))
        win.add_action(menu, ActionData(command_id='cmd_switch_environment', title='Switch Environment', icon='chain',
                                        tooltip='Switch runtime environment'))
        win.add_action(menu, ActionData(command_id='cmd_spatial_relationship_of_two_lines',
                                        title='Spatial Relationship of Two Lines',
                                        icon='cat-48',
                                        tooltip='Infer spatial relationship of the given two lines'))
