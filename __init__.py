# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name" : "Capifier",
    "author" : "PK",
    "version": (0, 0, 4),
    "description" : "Simple plugin to add proper cap quad topology to cylinders",
    "blender" : (2, 80, 0),
    "location" : "View3D > Edit Mode(Face) > Specials > Capify",
    "warning" : "",
    "category" : "Mesh"
}

if "bpy" in locals():
    import importlib
    importlib.reload(ui)
else:
    from capifier import ui

import bpy

def register():
    ui.register()

def unregister():
    ui.unregister()

if __name__ == "__main__":
    register()
