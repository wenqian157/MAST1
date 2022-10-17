import sys

#change this path to point to where your local mola folder is saved
path = "C:\D\GitHub"
if path not in sys.path:
    sys.path.append(path)

import mola
import random
from mola import module_rhino

## input from grasshopper, assign value here if it is run without grasshopper
# seed
# iteration
# mesh

## output
# mesh

random.seed(seed)

mesh = mola.Mesh()
a = mesh.add_vertex(0,0,0)
b = mesh.add_vertex(100,0,0)
c = mesh.add_vertex(100,100,0)
d = mesh.add_vertex(0,100,0)

mesh.add_face([a,b,c,d])

#step 1 : subdivide to center point
new_mesh = mola.Mesh()

for f in mesh.faces:
    new_faces = mola.subdivide_face_extrude_to_point_center(f,0)
    new_mesh.faces.extend(new_faces)

mesh = new_mesh

#step 2 : catmull
mesh.update_topology()
mesh = mola.subdivide_mesh_catmull(mesh)

#step 3: split grid
new_mesh = mola.Mesh()
for f in mesh.faces:
    new_faces = mola.subdivide_face_split_grid(f,2,1)
    new_mesh.faces.extend(new_faces)
mesh = new_mesh

#asign to all the same group
for f in mesh.faces:
    f.group = "plot"

new_mesh = mola.Mesh()

for f in mesh.faces:
    if f.group == "plot":
        new_faces = mola.subdivide_face_extrude_tapered(f, 0.0, 0.45, True)

        for nf in new_faces[:-1]:
            nf.group = "circulation"
            nf.color = (1,0,0)
        
        new_faces[-1].group = "construction"
        new_faces[-1].color = (0.5,0,1)
        new_mesh.faces.extend(new_faces)
    else:
            new_mesh.faces.append(f)

mesh = new_mesh
new_mesh = mola.Mesh()

for f in mesh.faces:
    if f.group == "construction":
            
        if random.random() < 0.2:
            # make a park
            new_faces = mola.subdivide_face_extrude_to_point_center(f, 10)
            for nf in new_faces:
                nf.group = "park"
                nf.color = (0,1,0)
            new_mesh.faces.extend(new_faces)
        else:
            # make a building
            floors = random.randint(5,15)
            temp = f
            for i in range(floors):
                fraction = random.randint(-2, 2) * 0.1
                new_faces = mola.subdivide_face_extrude_tapered(temp, 3, fraction, doCap = True)
                for nf in new_faces[:-1]:
                    nf.group = "facade"
                    nf.color = (0,1,1)
                new_faces[-1].group = "floor"
                temp = new_faces[-1]
                if i == floors-1:
                    new_faces[-1].group = "roof"
                    new_faces[-1].color = (1,0,1)
                new_mesh.faces.extend(new_faces)
    else:
            new_mesh.faces.append(f)

mesh = new_mesh
new_mesh = mola.Mesh()

for f in mesh.faces:
    if f.group == 'facade':
        # divide facade into panels
        mesh.update_topology()
        v1 = f.vertices[0]
        v2 = f.vertices[1]
        facade_length = mola.vertex_distance(v1,v2)
        num_subdivisions = int(facade_length/2)
        if num_subdivisions>1:
            new_faces = mola.subdivide_face_split_grid(f,num_subdivisions,1)
            for nf in new_faces:
                nf.group = "panel"
                nf.color = (0,0.2,0.8)
            new_mesh.faces.extend(new_faces)
        else:
            f.group = "panel"
            f.color = (0,0.2,0.8)
            new_mesh.faces.append(f)
    else:
            new_mesh.faces.append(f)

mesh = new_mesh
new_mesh = mola.Mesh()

for f in mesh.faces:
    if f.group =='panel':
        # details on the facade
        if random.random()<0.5:
            # make a solid pyramid
            new_faces = mola.subdivide_face_extrude_to_point_center(f,0.01)
            for nf in new_faces:
                nf.group = "solid"
                nf.color = (0,0.1,0.1)
            new_mesh.faces.extend(new_faces)
        else:
            # make a window
            new_faces = mola.subdivide_face_extrude_tapered(f, 0.01, 0.1, doCap = True)
            for nf in new_faces[:-1]:
                    nf.group = "frame"
                    nf.color = (0,0,0)
            new_faces[-1].group = "glass"
            new_faces[-1].color = (1,1,1)
            new_mesh.faces.extend(new_faces)
    else:
            new_mesh.faces.append(f)


a = module_rhino.display_mesh(new_mesh)
# mola.export_obj(mesh)