# -*- coding: utf-8 -*-

from command import CommandBase

from .infer_spatial_relationship_dialog import InferSpatialRelationshipDialog


class InferSpatialRelationshipCommand(CommandBase):

    def exec(self, *args, **kwargs):
        dialog = InferSpatialRelationshipDialog.get_dialog()
        dialog.show()
