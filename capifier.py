from math import (pi)
import bpy
import bmesh
from mathutils import (Vector)


def get_sorted_verts_list(verts_seq, projected_dirvec, center):
    verts = verts_seq[:]

    #find vertice that is closest to desired direction
    vangle = 2 * pi
    vindex = 0
    for i, v in enumerate(verts):
        proj_angle = projected_dirvec.angle(v.co - center)
        if proj_angle < vangle:
            vangle = proj_angle
            vindex = i
    #rotate list, so first vert is in proper direction
    return verts[vindex:] + verts[:vindex]

def calc_dir_vec(f):
    norm = f.normal
    zvec = Vector((0.0, 0.0, 1.0))
    dirvec = Vector((1.0, 0.0, 0.0))

    if norm.angle(zvec) > pi / 8:
        dirvec = Vector((0.0, 0.0, 1.0))

    return dirvec - norm.project(dirvec)

def capify(f, bm):
    verts = f.verts
    nverts = len(f.verts)
    if nverts % 8 != 0:
        return

    projected_dirvec = calc_dir_vec(f)

    center = Vector((0.0, 0.0, 0.0))
    for v in verts:
        center += v.co

    center = center / nverts

    verts = get_sorted_verts_list(verts, projected_dirvec, center)

    nverts2 = int(nverts / 2)
    nverts4 = int(nverts / 4)
    vpairs = []
    vpairs.append([verts[0], verts[nverts2]])
    vpairs.append([verts[nverts4], verts[nverts4 + nverts2]])
    for i in range(int((nverts4 - 2) / 2)):
        vpairs.append([verts[i + 1], verts[nverts2 - (i + 1) ]])
        vpairs.append([verts[nverts - (i + 1)], verts[nverts2 + (i + 1)]])
        vpairs.append([verts[nverts4 + i + 1], verts[nverts4 + nverts2 - (i + 1) ]])
        vpairs.append([verts[nverts4 - (i + 1)], verts[nverts2 + nverts4 + (i + 1)]])

    sel_verts = verts[:]

    bpy.ops.mesh.select_mode(type='VERT')
    for p in vpairs:
        bpy.ops.mesh.select_all(action='DESELECT')
        p[0].select_set(True)
        p[1].select_set(True)
        bpy.ops.mesh.vert_connect()
        sel_verts += [v for v in bm.verts if v.select]

    for v in sel_verts:
        v.select_set(True)

    bpy.ops.mesh.select_mode(type='FACE', use_extend=True)


class Capifier(bpy.types.Operator):
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
        sel = [f for f in bm.faces if f.select]
        for f in sel:
            capify(f, bm)
        return {"FINISHED"}


def special_menu_func(self, context):
    is_face_mode = context.tool_settings.mesh_select_mode[2]
    if is_face_mode:
        self.layout.separator()
        self.layout.operator("mesh.capify")

def face_menu_func(self, context):
    self.layout.separator()
    self.layout.operator("mesh.capify")

def register():
    bpy.utils.register_class(Capifier)
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(special_menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(face_menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(special_menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_faces.remove(face_menu_func)
    bpy.utils.unregister_class(Capifier)


if __name__ == '__main__':
    register()