import bpy
from capifier import ui

bl_info = {
    "name": "Capifier",
    "author": "PK",
    "version": (0, 0, 4),
    "description": "Simple plugin to add proper cap quad topology to cylinders",
    "blender": (2, 80, 0),
    "location": "View3D > Edit Mode(Face) > Specials > Capify",
    "warning": "",
    "category": "Mesh"
}


def register():
    ui.register()


def unregister():
    ui.unregister()

if __name__ == "__main__":
    register()
