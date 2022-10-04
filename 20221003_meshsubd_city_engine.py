#region FOR RUNNING IN CODE LISTENER
import sys
import os
# SCRIPT_DIR = os.path.dirname(__file__)
# sys.path.append(os.path.dirname(SCRIPT_DIR))
path = "C:\D\GitHub"
if path not in sys.path:
    sys.path.append(path)
#endregion

import mola
import random
from mola import Engine

mesh_city = mola.Mesh()

a = mesh_city.add_vertex(0, 0, 0)
b = mesh_city.add_vertex(274, 0, 0)
c = mesh_city.add_vertex(274, 80, 0)
d = mesh_city.add_vertex(0, 80, 0)
mesh_city.add_face([a, b, c, d])
mesh_city.faces[0].group = "block"

# mesh_city = module_rhino.mesh_from_rhino_mesh(mesh)
# make plots
def my_filter(face):
    return face.group == "block"

def my_rule(face):
    return mola.subdivide_face_split_grid(face, 8, 3)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        for f in faces:
            f.group = "block"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, my_rule, my_labeling)

def my_filter(face):
    return face.group == "block"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 0, 0.2)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_index(faces, "road", "up")
    # for faces in divided_faces:
    #     for f in faces:
    #         f.group = "road"
    #     faces[-1].group = "up"
    for f in undivided_faces:
        f.group = "road"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, my_rule, my_labeling, 0.8)

# grow up 
def my_filter(face):
    return face.group == "up"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 3, 0)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_orientation(faces, "up", "down", "side")
    for f in undivided_faces:
        f.group = "roof"

for _ in range(20):
    mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, my_rule, my_labeling, 0.8)

# make facade
def my_filter(face):
    return face.group == "side"

def my_rule(face):
    return mola.subdivide_face_split_cell(face, 1, 3)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_default(faces, "side")
    for f in undivided_faces:
        f.group = "wall"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, my_rule, my_labeling, 0.8)


def my_filter(face):
    return face.group == "side"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 0, 0.3)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_index(faces, "frame", "glass")
    for f in undivided_faces:
        f.group = "panel"

mesh_city.faces = Engine.subdivide(mesh_city.faces, my_filter, my_rule, my_labeling, 0.8)

mola.color_by_group(mesh_city.faces)

from mola import module_rhino
a = module_rhino.display_mesh(mesh_city)