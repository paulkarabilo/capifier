import bpy
import bmesh
from .capify import (capify, is_cap)
from bpy.props import FloatProperty

class CapifierOperator(bpy.types.Operator):
    bl_idname = "mesh.capify"
    bl_label = "Capify"
    bl_context = "objectmode"
    bl_description = "Add proper topology to cylinder object caps"
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
        return (ob and ob.type == 'MESH' and (
                context.mode == 'OBJECT' or context.mode == 'EDIT_MESH'))

    def execute(self, context):
        must_reset = False
        if context.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode="EDIT")
            bm = bmesh.from_edit_mesh(context.active_object.data)
            sel = [f for f in bm.faces if is_cap(f)]
            must_reset = True
        else:
            bm = bmesh.from_edit_mesh(context.active_object.data)
            sel = [f for f in bm.faces if f.select and is_cap(f)]
        for f in sel:
            capify(f, bm, self.rotation)
        if must_reset:
            bpy.ops.object.mode_set(mode="OBJECT")
        return {'FINISHED'}
