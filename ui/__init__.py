import bmesh
import bpy
from .face import FaceCapifier
from .object import ObjectCapifier

def is_cap(face):
    return True

def applicable_faces_selected(faces):
    for f in faces:
        if is_cap(f):
            return True
    return False

def applicable_object_selected(obj):
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    res = applicable_faces_selected(bm.faces)
    bpy.ops.object.mode_set(mode='OBJECT')
    return res

def special_menu_func(self, context):
    is_face_mode = context.tool_settings.mesh_select_mode[2]
    if is_face_mode and applicable_faces_selected(bmesh.from_edit_mesh(context.active_object.data)):
        self.layout.separator()
        self.layout.operator(FaceCapifier.bl_idname)

def face_menu_func(self, context):
    if (applicable_faces_selected(f for f in bmesh.from_edit_mesh(context.active_object.data).faces if f.select)):
        self.layout.separator()
        self.layout.operator(FaceCapifier.bl_idname)

def object_menu_func(self, context):
    if (applicable_object_selected(bpy.context.active_object)):
        self.layout.separator()
        self.layout.operator(ObjectCapifier.bl_idname)

def register():
    bpy.utils.register_class(FaceCapifier)
    bpy.utils.register_class(ObjectCapifier)
    bpy.types.VIEW3D_MT_object_specials.append(object_menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(special_menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(face_menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(special_menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_faces.remove(face_menu_func)
    bpy.types.VIEW3D_MT_object_specials.remove(object_menu_func)
    bpy.utils.unregister_class(ObjectCapifier)
    bpy.utils.unregister_class(FaceCapifier)

if __name__ == '__main__':
    register()
