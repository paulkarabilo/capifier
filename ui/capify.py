import bpy
import bmesh
from mathutils import Vector
from math import pi

def is_cap(f):
    verts = f.verts
    nverts = len(f.verts)
    if nverts % 8 != 0:
        return False
    center = Vector((0.0, 0.0, 0.0))
    for v in verts:
        center += v.co

    center = center / nverts
    dist = (verts[0].co - center).length
    for v in verts:
        if (abs((v.co - center).length - dist) > 0.1):
            return False
    return True

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

    bpy.ops.mesh.select_mode(type='FACE', use_extend=True, use_expand=True)
