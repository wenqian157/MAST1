#region FOR RUNNING IN CODE LISTENER
import sys
import os

path = "C:\D\GitHub"
if path not in sys.path:
    sys.path.append(path)
#endregion

import mola
import random
from mola import Engine
from mola import module_rhino

mola_mesh = module_rhino.mesh_from_rhino_mesh(rhino_mesh)

mola_mesh.update_topology()
Engine.group_by_orientation(mola_mesh.faces, "up", "down", "side")

for f in mola_mesh.faces:
    if f.group == "side":
        if abs(f.center().x) <= dist_x and abs(f.center().y) <= dist_y:
            f.group = "side_in"
        else: 
            f.group = "side_out"
            

def my_filter(face):
    return face.group == "side_in"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 0, 0.3)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_index(faces, "frame", "glass")
    for f in undivided_faces:
        f.group = "wall"

mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling, 0.8)


def my_filter(face):
    return face.group == "up" and face.center().z <= 10

def my_rule(face):
    return mola.subdivide_face_split_grid(face, 2, 2)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_default(faces, "up")
    for f in undivided_faces:
        f.group = "roof"
mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling, 0.8)


def my_filter(face):
    return face.group == "up" and face.center().z <= 10

def my_rule(face):
    return mola.subdivide_face_extrude(face, 2)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_orientation(faces, "up", "wall", "wall")
    for f in undivided_faces:
        f.group = "roof"

for _ in range(6):
    mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling, 0.6)


# for f in mola_mesh.faces:
#     f.group = "block"

# # make plots
# def my_filter(face):
#     return face.group == "block"

# def my_rule(face):
#     return mola.subdivide_face_split_grid(face, 8, 3)

# def my_labeling(divided_faces, undivided_faces):
#     for faces in divided_faces:
#         for f in faces:
#             f.group = "block"

# mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling)

# def my_filter(face):
#     return face.group == "block"

# def my_rule(face):
#     return mola.subdivide_face_extrude_tapered(face, 0, 0.2)

# def my_labeling(divided_faces, undivided_faces):
#     # for faces in divided_faces:
#     #     Engine.group_by_index(faces, "road", "up")
#     for faces in divided_faces:
#         for f in faces[:-1]:
#             f.group = "road"
#         faces[-1].group = "up"
#     for f in undivided_faces:
#         f.group = "road"

# mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling, 0.8)

# # grow up 
# def my_filter_up(face):
#     return face.group == "up"

# def my_rule_up(face):
#     return mola.subdivide_face_extrude_tapered(face, 5, 0)

# def my_labeling_up(divided_faces, undivided_faces):
#     for faces in divided_faces:
#         Engine.group_by_orientation(faces, "up", "down", "side")

#     for f in undivided_faces:
#         f.group = "roof"

# def my_filter_side(face):
#     return face.group == "side"

# def my_rule_side(face):
#     return mola.subdivide_face_extrude_tapered(face, 5, 0)

# def my_labeling_side(divided_faces, undivided_faces):
#     for faces in divided_faces:
#         Engine.group_by_orientation(faces, "up", "down", "side")
#     for f in undivided_faces:
#         f.group = "wall"

# for _ in range(18):
#     mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter_up, my_rule_up, my_labeling_up, 0.85)
#     mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter_side, my_rule_side, my_labeling_side, 0.05)


# # make facade

# for f in mola_mesh.faces:
#     if f.group == "side":
#         f.group = "wall"

# def my_filter(face):
#     return face.group == "wall"

# def my_rule(face):
#     return mola.subdivide_face_split_cell(face, 1, 3)

# def my_labeling(divided_faces, undivided_faces):
#     for faces in divided_faces:
#         for f in faces:
#             f.group = "wall"
#     for f in undivided_faces:
#         f.group = "wall"

# mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling, 0.8)


# def my_filter(face):
#     return face.group == "wall"

# def my_rule(face):
#     return mola.subdivide_face_extrude_tapered(face, 0, 0.3)

# def my_labeling(divided_faces, undivided_faces):
#     for faces in divided_faces:
#         Engine.group_by_index(faces, "frame", "glass")
#     for f in undivided_faces:
#         f.group = "panel"

# mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling, 0.8)

mola.color_by_group(mola_mesh.faces)
a = module_rhino.display_mesh(mola_mesh)