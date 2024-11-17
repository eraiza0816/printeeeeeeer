from stl import mesh
import numpy as np

# Define dimensions
width = 97.0  # mm
height = 129.0  # mm
depth = 3.0  # mm

# Define vertices of the rectangular prism (thin plate)
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

# Define the faces of the rectangular prism
faces = np.array([
    [0, 1, 2], [0, 2, 3],  # bottom
    [4, 5, 6], [4, 6, 7],  # top
    [0, 1, 5], [0, 5, 4],  # front
    [2, 3, 7], [2, 7, 6],  # back
    [1, 2, 6], [1, 6, 5],  # right
    [3, 0, 4], [3, 4, 7]   # left
])

# Create the mesh
plate_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, face in enumerate(faces):
    for j in range(3):
        plate_mesh.vectors[i][j] = vertices[face[j], :]

# Save the mesh to file
plate_mesh.save('plate_97x129x3mm.stl')
