# -*- coding: utf-8 -*-

from command import register_command
from shared.context import Context
from ui import ActionData, MenuData

from .clean_log_files import CleanLogFilesCommand
from .switch_environment import SwitchEnvironmentCommand
from .infer_spatial_relationship import InferSpatialRelationshipCommand


def initialize(ctx: Context):
    register_command(
        command_id='cmd_clean_log_files',
        command=CleanLogFilesCommand(),
        name='Clean Log Files'
    )
    register_command(
        command_id='cmd_switch_environment',
        command=SwitchEnvironmentCommand(),
        name='Switch Environment'
    )
    register_command(
        command_id='cmd_infer_spatial_relationship',
        command=InferSpatialRelationshipCommand(),
        name='Infer Spatial Relationship'
    )

    menu = MenuData('Glodon', [
        ActionData(
            command_id='cmd_clean_log_files',
            title='Clean Log Files',
            icon='clean',
            tooltip='Clean log files under architecture and structure software package'
        ),
        ActionData(
            command_id='cmd_switch_environment',
            title='Switch Environment',
            icon='chain',
            tooltip='Switch runtime environment'
        ),
        ActionData(
            command_id='cmd_infer_spatial_relationship',
            title='Infer Spatial Relationship',
            icon='perpendicular',
            tooltip='Infer spatial relationship of two given line segments'
        )
    ])
    ctx.main_window.add_menu(menu)
