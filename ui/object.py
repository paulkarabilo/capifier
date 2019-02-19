import bpy
import bmesh 

class ObjectCapifier(bpy.types.Operator):
    bl_idname = "object.capify"
    bl_label = "Capify"
    bl_context = "objectmode"
    bl_description = "Add proper topology to cylinder object caps"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return (ob and ob.type == 'MESH' and context.mode == 'OBJECT')

    def execute(self, context):
        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(context.active_object.data)
        return {'FINISHED'}