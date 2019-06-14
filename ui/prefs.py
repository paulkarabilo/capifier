from os import path
import bpy
from bpy.props import *
import rna_keymap_ui
from .face import FaceCapifier

def has_mapping(km, kmi_name):
    for i, km_item in enumerate(km.keymap_items):
      if km.keymap_items.keys()[i] == kmi_name:
        return km_item
    return None

class CapifierPreferences(bpy.types.AddonPreferences):
  bl_idname = "capifier"

  def draw(self, context):
    layout = self.layout
    col = layout.column(align=True)

    kc = bpy.context.window_manager.keyconfigs.user

    km = kc.keymaps['3D View']
    kmi = has_mapping(km, FaceCapifier.bl_idname)
    if kmi:
        col.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
