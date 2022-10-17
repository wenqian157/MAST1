#region FOR RUNNING IN CODE LISTENER
import sys


path = "C:\D\GitHub"
if path not in sys.path:
    sys.path.append(path)
#endregion

import mola
import random
from mola import Engine


# mola_mesh = module_rhino.mesh_from_rhino_mesh(rhino_mesh)
# mola_mesh = mola.Mesh()

# a = mola_mesh.add_vertex(0, 0, 0)
# b = mola_mesh.add_vertex(274, 0, 0)
# c = mola_mesh.add_vertex(274, 80, 0)
# d = mola_mesh.add_vertex(0, 80, 0)
# mola_mesh.add_face([a, b, c, d])
# print(mola_mesh.faces[0].group)


mola_circle = mola.construct_circle(100, 8)
mola_mesh = mola.Mesh()
mola_mesh.add_vertex(0, 0, 0)
for v in mola_circle:
    mola_mesh.vertices.append(v)


for i in range(len(mola_circle)):
    mola_mesh.add_face([mola_mesh.vertices[0], mola_mesh.vertices[i+1], mola_mesh.vertices[(i+1)%(len(mola_circle))+1]])

