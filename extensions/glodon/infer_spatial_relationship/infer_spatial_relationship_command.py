# -*- coding: utf-8 -*-

from command import ICommand

from .infer_spatial_relationship_dialog import InferSpatialRelationshipDialog


class InferSpatialRelationshipCommand(ICommand):

    def exec(self, *args, **kwargs):
        dialog = InferSpatialRelationshipDialog.get_dialog()
        dialog.show()
