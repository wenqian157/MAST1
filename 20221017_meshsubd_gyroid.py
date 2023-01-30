#region FOR RUNNING IN CODE LISTENER
import sys

path = "C:\D\GitHub"
if path not in sys.path:
    sys.path.append(path)
#endregion

import mola
from mola import Engine
from mola import module_rhino

mola_mesh = module_rhino.mesh_from_rhino_mesh(rhino_mesh)

dist_in_sq = dist_in ** 2
dist_out_sq = dist_out ** 2

Engine.group_by_orientation(mola_mesh.faces, "up", "down", "side")

for f in mola_mesh.faces:
    if f.group == "side":
        dist_sq = f.center().x**2 + f.center().y**2
        if dist_sq > dist_out_sq:
            f.group = "side_out"
        elif dist_sq < dist_in_sq:
            f.group = "side_in"

def my_filter(face):
    return face.group == "side_out"

def my_rule(face):
    return mola.subdivide_face_extrude_tapered(face, 4, 0.5)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_index(faces, "frame", "glass")
    for f in undivided_faces:
        f.group = "wall"

mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling, 0.8)


def my_filter(face):
    return face.group == "side_in"

def my_rule(face):
    return mola.subdivide_face_extrude(face, 10)

def my_labeling(divided_faces, undivided_faces):
    for faces in divided_faces:
        Engine.group_by_default(faces, "bridge")
    for f in undivided_faces:
        f.group = "side_in"

mola_mesh.faces = Engine.subdivide(mola_mesh.faces, my_filter, my_rule, my_labeling, 0.2)


mola.color_by_group(mola_mesh.faces)
# a = module_rhino.display_mesh(mola_mesh)

# export group seperately
groups = []
for f in mola_mesh.faces:
    if not (f.group in groups):
        groups.append(f.group)

rhino_meshes = []
for i in range(len(groups)):
    new_mesh = mola.Mesh()
    for f in mola_mesh.faces:
        if f.group == groups[i]:
            new_mesh.faces.append(f)
    rhino_meshes.append(module_rhino.display_mesh(new_mesh))

a = rhino_meshes
