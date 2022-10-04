#region FOR RUNNING IN CODE LISTENER
# import sys
# import os 

# path = os.path.dirname(os.path.dirname(__file__))
# if path not in sys.path:
#     sys.path.append(path)
#endregion

import mola
from mola import module_rhino
import math


my_sphere = mola.construct_sphere(radius=5,u_res=8,v_res=8)
for v in my_sphere.vertices:  # turn sphere into egg
    if (v.z>0):
        v.z *= 1.8

my_sphere = mola.subdivide_mesh_catmull(my_sphere)

#region GET ATTRIBUTES

face_angles = my_sphere.face_properties(mola.face_angle_vertical)

for i in range(len(face_angles)):
    face_angles[i] = abs(math.pi - abs(face_angles[i]))
face_angles = mola.math_map_list(face_angles, 0.1, 2)

# analyse z positions of faces
z_positions = my_sphere.face_properties(mola.face_center_z)

#larger opening the larger z
fractions = mola.math_map_list(z_positions,0.9,0.1)

# closed when below 0.2 (=20%)
doCaps = [True] * len(my_sphere.faces)
for i in range(len(z_positions)):
    if z_positions[i] > 0.2:
        doCaps[i] = False

#endregion

# # colorise mesh    
# mola.color_faces_by_values(my_sphere.faces, z_positions)

# parametric subdivision based on the analyses
# deeper opening when vertical face, large opening when higher, closed on the bottom
my_sphere = mola.subdivide_mesh_extrude_tapered(my_sphere, face_angles, fractions, doCaps)

#region OFFSET AND SMOOTH
# smooth result
my_sphere = mola.subdivide_mesh_catmull(my_sphere)

# turn into volume by offset
my_sphere = mola.mesh_offset(my_sphere,0.1)

my_sphere = mola.subdivide_mesh_catmull(my_sphere)
#endregion

colors = my_sphere.face_properties(mola.face_center_z)
mola.color_faces_by_values(my_sphere.faces, colors)

a = module_rhino.display_mesh(my_sphere)



