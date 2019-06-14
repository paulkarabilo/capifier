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

addon_keymaps = []

def register_keymap():

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if not kc:
        return

    km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.new(FaceCapifier.bl_idname, "C", "PRESS", shift=True, ctrl=True)
    kmi.properties.name = "FaceCapifier"
    addon_keymaps.append((km, kmi))

def unregister_keymap():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


def register():
    bpy.utils.register_class(FaceCapifier)
    bpy.utils.register_class(ObjectCapifier)
    bpy.types.VIEW3D_MT_object_context_menu.append(object_menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(special_menu_func)
    register_keymap()

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(special_menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.remove(object_menu_func)
    bpy.utils.unregister_class(ObjectCapifier)
    bpy.utils.unregister_class(FaceCapifier)
    unregister_keymap()

if __name__ == '__main__':
    register()
