import bpy
import bmesh
from .capify import (capify, is_cap)

class FaceCapifier(bpy.types.Operator):
    bl_idname = "mesh.capify"
    bl_label = "Capify"
    bl_context = "mesh_edit"
    bl_description = "Add proper topology to circular faces (cylinder caps)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')

    def execute(self, context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        sel = [f for f in bm.faces if f.select and is_cap(f)]
        for f in sel:
            capify(f, bm)
        return {"FINISHED"}
