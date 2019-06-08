import bmesh
import bpy
from .face import FaceCapifier
from .object import ObjectCapifier

def special_menu_func(self, context):
    is_face_mode = context.tool_settings.mesh_select_mode[2]
    if is_face_mode:
        self.layout.separator()
        self.layout.operator(FaceCapifier.bl_idname)

def object_menu_func(self, context):
    self.layout.separator()
    self.layout.operator(ObjectCapifier.bl_idname)

def register():
    bpy.utils.register_class(FaceCapifier)
    bpy.utils.register_class(ObjectCapifier)
    bpy.types.VIEW3D_MT_object_context_menu.append(object_menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(special_menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(special_menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.remove(object_menu_func)
    bpy.utils.unregister_class(ObjectCapifier)
    bpy.utils.unregister_class(FaceCapifier)

if __name__ == '__main__':
    register()
