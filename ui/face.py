import bpy
import bmesh
from .capify import (capify, is_cap)

from bpy.props import (FloatProperty)

class FaceCapifier(bpy.types.Operator):
    bl_idname = "mesh.capify"
    bl_label = "Capify"
    bl_context = "mesh_edit"
    bl_description = "Add proper topology to circular faces (cylinder caps)"
    bl_options = {"REGISTER", "UNDO"}

    rotation: FloatProperty(
        attr='rotation',
        name='Rotation',
        default=0,
        min=0,
        max=360,
        description='Adjust cap geometry rotation'
    )

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        sel = [f for f in bm.faces if f.select and is_cap(f)]
        for f in sel:
            capify(f, bm, self.rotation)
        return {"FINISHED"}

    def invoke(self, context, event):
        self.execute(context)

        return {'FINISHED'}