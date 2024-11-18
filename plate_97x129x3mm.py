# Import necessary libraries
from stl import mesh
import numpy as np

# Define dimensions of the plate (rectangular prism)
width = 97.0  # mm
height = 129.0  # mm
depth = 3.0  # mm

# Define vertices of the rectangular prism (thin plate) using numpy array
vertices = np.array([
    [0, 0, 0],
    [width, 0, 0],
    [width, height, 0],
    [0, height, 0],
    [0, 0, depth],
    [width, 0, depth],
    [width, height, depth],
    [0, height, depth]
])

# Define the faces of the rectangular prism using numpy array
faces = np.array([
    [0, 1, 2], [0, 2, 3],  # bottom
    [4, 5, 6], [4, 6, 7],  # top
    [0, 1, 5], [0, 5, 4],  # front
    [2, 3, 7], [2, 7, 6],  # back
    [1, 2, 6], [1, 6, 5],  # right
    [3, 0, 4], [3, 4, 7]   # left
])

# Create the mesh by initializing an empty mesh object with the correct number of faces and vertices
plate_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

# Iterate over each face in the faces array
for i, face in enumerate(faces):
    # Iterate over each vertex index in the current face
    for j in range(3):
        # Assign the corresponding vertex coordinates to the mesh object's vector
        plate_mesh.vectors[i][j] = vertices[face[j], :]


# Save the mesh object to a file with the specified filename
plate_mesh.save('plate_97x129x3mm.stl')
