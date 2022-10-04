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

## output
# my_city

random.seed(seed)

def subdivide_by_group(mesh):
    
    newMesh = mola.Mesh()
    
    for f in mesh.faces:
        if f.group == "plot":
            
            newFaces = mola.subdivide_face_extrude_tapered(f, 0.0, 0.45, True)
            for nf in newFaces[:-1]:
                nf.group = "circulation"
                nf.color = (1,0,0)
            newFaces[-1].group = "construction"
            newFaces[-1].color = (0.5,0,1)
            newMesh.faces.extend(newFaces)
        elif f.group == "construction":
            
            if random.random() < 0.2:
                # make a park
                newFaces = mola.subdivide_face_extrude_to_point_center(f, 10)
                for nf in newFaces:
                    nf.group = "park"
                    nf.color = (0,1,0)
                newMesh.faces.extend(newFaces)
            else:
                # make a building
                floors = random.randint(5,15)
                temp = f
                for i in range(floors):
                    fraction = random.randint(-2, 2) * 0.1
                    newFaces = mola.subdivide_face_extrude_tapered(temp, 3, fraction, doCap = True)
                    for nf in newFaces[:-1]:
                        nf.group = "facade"
                        nf.color = (0,1,1)
                    newFaces[-1].group = "floor"
                    temp = newFaces[-1]
                    if i == floors-1:
                        newFaces[-1].group = "roof"
                        newFaces[-1].color = (1,0,1)
                    newMesh.faces.extend(newFaces)
                    
        elif f.group == 'facade':
            # divide facade into panels
            mesh.update_topology()
            v1 = f.vertices[0]
            v2 = f.vertices[1]
            facade_length = mola.vertex_distance(v1,v2)
            num_subdivisions = int(facade_length/2)
            if num_subdivisions>1:
                newFaces = mola.subdivide_face_split_grid(f,num_subdivisions,1)
                for nf in newFaces:
                    nf.group = "panel"
                    nf.color = (0,0.2,0.8)
                newMesh.faces.extend(newFaces)
            else:
                f.group = "panel"
                f.color = (0,0.2,0.8)
                newMesh.faces.append(f)
                
        elif f.group =='panel':
            # details on the facade
            if random.random()<0.5:
                # make a solid pyramid
                newFaces = mola.subdivide_face_extrude_to_point_center(f,0.01)
                for nf in newFaces:
                    nf.group = "solid"
                    nf.color = (0,0.1,0.1)
                newMesh.faces.extend(newFaces)
            else:
                # make a window
                newFaces = mola.subdivide_face_extrude_tapered(f, 0.01, 0.1, doCap = True)
                for nf in newFaces[:-1]:
                        nf.group = "frame"
                        nf.color = (0,0,0)
                newFaces[-1].group = "glass"
                newFaces[-1].color = (1,1,1)
                newMesh.faces.extend(newFaces)
        else:
            newMesh.faces.append(f)
    
    return newMesh
    

my_city = mola.Mesh()
a = my_city.add_vertex(0,0,0)
b = my_city.add_vertex(100,0,0)
c = my_city.add_vertex(100,100,0)
d = my_city.add_vertex(0,100,0)

my_city.add_face([a,b,c,d])


#step 1 : subdivide to center point
newMesh = mola.Mesh()

for f in my_city.faces:
    newFaces = mola.subdivide_face_extrude_to_point_center(f,0)
    newMesh.faces.extend(newFaces)

my_city = newMesh

#step 2 : catmull
my_city.update_topology()
my_city = mola.subdivide_mesh_catmull(my_city)

#step 3: split grid
newMesh = mola.Mesh()
for f in my_city.faces:
    newFaces = mola.subdivide_face_split_grid(f,2,1)
    newMesh.faces.extend(newFaces)
my_city = newMesh

#asign to all the same group
for f in my_city.faces:
    f.group = "plot"

#step 4 : make my city
for i in range(iteration):
    
    my_city = subdivide_by_group(my_city)

a = module_rhino.display_mesh(my_city)
# mola.export_obj(my_city)