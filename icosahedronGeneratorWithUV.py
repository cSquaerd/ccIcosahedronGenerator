import scipy.constants as spc
import math
import json
# Compute u - v
def vecDiff(u, v):
	if type(u) is not list and type(v) is not list and len(u) != len(v):
		raise TypeError("Arguements must be lists of the same size.")
	return list( \
		map( \
			lambda m, n : m - n, \
			u, \
			v, \
		) \
	)
# Compute u . v
def dotProd(u, v):
	if type(u) is not list and type(v) is not list and len(u) != len(v):
		raise TypeError("Arguements must be lists of the same size.")
	return sum( \
		map( \
			lambda m, n : m * n, \
			u, \
			v, \
		) \
	)
# Compute ||v||
def eucNorm(v):
	return dotProd(v, v) ** 0.5
# Compute v / ||v||
def normalize(v):
	n = eucNorm(v)
	return list( \
		map( \
			lambda i : round(i / n, 10), \
			v \
		) \
	)
# Compute u x v
def crossProd(u, v):
	# Remember: x:0, y:1, z:2
	return [\
		u[1] * v[2] - u[2] * v[1], \
		- (u[0] * v[2] - u[2] * v[0]), \
		u[0] * v[1] - u[1] * v[0] \
	]
# Get the vertex IDs neighboring a given vertex
def getNeighbors(n):
	global edges
	pairsNFirst = edges[5*n:5*n+5]
	return tuple( \
		map( \
			lambda p : p[1], \
			pairsNFirst
		) \
	)
# Get the angle between two vectors
def vecAngle(u, v):
	return math.degrees(
		math.acos(
			dotProd(u, v) / (eucNorm(u) * eucNorm(v))
		)
	)
# Main code
# Generate the 12 vertices of the icosahedron
v = [spc.golden, 1, 0]
vertices = []
for j in range(4):
	# Copy the current vertex, and then
	# cycle the final coordinate around
	for k in range(3):
		vertices.append(v.copy())
		t = v.pop()
		v.insert(0, t)
	# After a full cycle, negate one coordinate
	v[(j + 2) % 2] *= -1
# Sort the vertices by y-coord and show them all
vertices.sort(key = lambda v : v[1])
for u in vertices:
	print(vertices.index(u), ':', u)
# Generate 60 (2 directions per) edges
edges = []
for u in vertices:
	for w in vertices:
		# Do not bother if vertices are the same
		if w != u:
			# Compute the direction vector, and check its length
			d = vecDiff(u, w)
			n = eucNorm(d)
			# Edges should be of length 2
			if round(n, 4) != 2.0000:
				continue
			edges.append((vertices.index(u), vertices.index(w)))
edges.sort()
# Show all edges; Each vertex should have five edges emitted from it
for e in edges:
	i = edges.index(e)
	print( \
		i, ':',  e, \
		end = '\n' if (i + 1) % 5 == 0 else '\t' \
	)
# Generate 20 triangle faces
triangles = []
# Go through each vertex
for n in range(12):
	# Get the neighboring vertices
	neighborsN = getNeighbors(n)
	for m in neighborsN:
		# Get the neighbors of each main neighbor
		neighborsM = getNeighbors(m)
		for k in neighborsM:
			# See if any of the third stage neighbors are
			# the original vertex; This means we have a triangle
			if n in getNeighbors(k):
				t = tuple(sorted([n + 1, m + 1, k + 1]))
				if t not in triangles:
					triangles.append(t)
				else:
					continue
			else:
				continue
for t in triangles:
	print(triangles.index(t) + 1, ':', t)
# Generate 20 normal vectors for the faces
triangleData = {}
neededCrossProdRedo = []
for t in triangles:
	# Get two edges of the triangle
	e1 = vecDiff(vertices[t[1] - 1], vertices[t[0] - 1])
	e2 = vecDiff(vertices[t[2] - 1], vertices[t[0] - 1])
	# Calculate the normal
	n = normalize(crossProd(e1, e2))
	# Check if the normal is pointing the right way
	if vecAngle(n, vertices[t[0] - 1]) > 90.0:
		# Fix the normal if its pointing the wrong way
		n = normalize(crossProd(e2, e1))
		# Mark the triangle for fixing later
		neededCrossProdRedo.append(triangles.index(t) + 1)
	triangleData[triangles.index(t) + 1] = { \
		"vertices" : t, \
		"normal": tuple(n) \
	}

print(neededCrossProdRedo)
# If a triangle needed its normal recalculated,
# the order of its vertices is wrong in terms of
# clockwise or counter-clockwise. Thus,
# the order of the vertices must be reversed;
# This can be done just by swapping any two vertices
for k in neededCrossProdRedo:
	temp = list(triangleData[k]["vertices"])
	a = temp[2]
	temp[2] = temp[1]
	temp[1] = a
	triangleData[k]["vertices"] = tuple(temp)
# Once all faces have their vertices known and in the right order,
# use the face-vertices pairs to assign every face the correct UV vertices

# Numeric representation of my own UV map (see github for picture)
aboveFaces = (1, 3, 5, 6, 8, 13, 14, 15, 16, 19)
aboveUVVertices = {n for n in range(1, 12)}
belowFaces = (2, 4, 7, 9, 10, 11, 12, 17, 18, 20)
belowUVVertices = {n for n in range(12, 25)}

leftFaces = (1, 3, 9, 10, 16, 17, 18, 19, 20)
leftUVVertices = {n for n in range(6, 19)}
rightFaces = (2, 4, 6, 7, 8, 11, 12, 13, 14)
rightUVVertices = {n for n in range(1, 7)} | {n for n in range(18, 25)}
# Measures of each equilateral triangle on UV Map
side = 0.25
height = math.tan(60 * math.pi / 180) / 8
# All coordinates of the 24 UV vertices
verticesUV = [
	(7 * side / 2, 3 * side - height), (5 * side / 2, 3 * side - height),
	(3 * side, 3 * side), (7 * side / 2, 3 * side + height),
	(5 * side / 2, 3 * side + height), (2 * side, 3 * side),
	(3 * side / 2, 3 * side + height), (side / 2, 3 * side + height),
	(side, 3 * side), (3 * side / 2, 3 * side - height),
	(side / 2, 3 * side - height), (side / 2, side + height),
	(3 * side / 2, side + height), (0, side),
	(side, side), (side / 2, side - height),
	(3 * side / 2, side - height), (2 * side, side),
	(5 * side / 2, side - height), (7 * side / 2, side - height),
	(3 * side, side), (1, side),
	(5 * side / 2, side + height), (7 * side / 2, side + height)
]
# One-to-Many relation between real vertices and possible UV vertices
realToUV = [
	{10, 19}, {3, 11, 20}, {4, 9, 12, 13}, {21},
	{2, 18}, {6, 22}, {5, 18}, {6, 14},
	{1, 9, 23, 24}, {15}, {3, 8, 16}, {7, 17}
]
#upUVVertices = [8, 20, 4, 21, 4, 5, 17, 5, 11, 12, 23, 22, 5, 5, 1, 1, 13, 17, 8, 14]
# Derive ordered UV vertices for every face
for face in triangleData.keys():
	realVertices = triangleData[face]["vertices"]
	# perform a Set Union to start
	possibleUVVertices = realToUV[realVertices[0] - 1] \
		| realToUV[realVertices[1] - 1] | realToUV[realVertices[2] - 1]
	print(
		'[' + format(face, " >2d") + "] All:",
		format(str(possibleUVVertices), " <32s"),
		end = ";\n"
	)
	# Filter out from the set based on +v/-v hemisphere
	if face in aboveFaces:
		possibleUVVertices = possibleUVVertices & aboveUVVertices
	else:
		possibleUVVertices = possibleUVVertices & belowUVVertices
	print("Filtered Above/Below", format(str(possibleUVVertices), " <16s"), end = "; ")
	# Filter out from the set based on +u/-u hemisphere
	if face in leftFaces:
		possibleUVVertices = possibleUVVertices & leftUVVertices
	elif face in rightFaces:
		possibleUVVertices = possibleUVVertices & rightUVVertices
	# Special cases on the pentagonal pyramids at the seam
	if face in (10, 11): # Lefthand faces (thus the actual vertices have locally low u values)
		possibleUVVertices = possibleUVVertices - {
			max(possibleUVVertices, key = lambda v : verticesUV[v - 1][0])
		}
	elif face in (9, 12): # Righthand faces (thus the actual vertices have locally high u values)
		possibleUVVertices = possibleUVVertices - {
			min(possibleUVVertices, key = lambda v : verticesUV[v - 1][0])
		}

	print("Filtered Full", format(str(possibleUVVertices), " <16s"), end = ";\n")
	# By here only 3 UV vertices remain, exactly enough;
	# They need to be in the same order as the real vertices though,
	# but it is known what real vertices correspond to which UV vertices,
	# so do an intersection per real vertex and use the sole element
	#orderedUVs = [
	#	tuple(possibleUVVertices.intersection(realToUV[r]))[0]
	#	for r in realVertices
	#]
	# Swap the two vertices that make an underline for the number (if this were a d20)
	# Otherwise the textures will appear mirrored
	#topVertexIndex = orderedUVs.index(upUVVertices[face])
	#swapIndices = list({0, 1, 2} - {topVertexIndex})
	#i = swapIndices[0]
	#j = swapIndices[1]
	#temp = orderedUVs[i]
	#orderedUVs[i] = orderedUVs[j]
	#orderedUVs[j] = temp

	#print("Real Vertices:", format(str(realVertices), " <20s"), end = "; ")
	#print("Ordered UV Vertices:", format(str(orderedUVs), " <20s"))

	triangleData[face]["UVs"] = list(possibleUVVertices)#orderedUVs

# Show all the triangle data, which is vertices (real and UV) and normals
for n in triangleData.keys():
	print(
		format(n, " >2d") + ": " \
		+ "vertices: " + format(str(triangleData[n]["vertices"]), " >11s") \
		+ "; UVs:" + format(str(triangleData[n]["UVs"]), " >15s") \
		+ "; normal:" + str(
			list(map(lambda x : round(x, 3), triangleData[n]["normal"]))
		)
	)
print("verticesUV Length:", len(verticesUV))
# Prompt to and possibly write out an obj 3D model file
if input("Write a new .obj file? [Y/n]: ").upper() == 'Y':
	objFile = open("ccIcosahedronWithUV.obj", 'w')
	for v in vertices:
		objFile.write("v " + ' '.join(map(str, v)) + '\n')
	for v in verticesUV:
		objFile.write("vt " + ' '.join(map(str, v)) + '\n')
	for k in range(1, 21):
		objFile.write("vn " + ' '.join(map(str, triangleData[k]["normal"])) + '\n')
	for k in range(1, 21):
		objFile.write("f ")
		face = triangleData[k]
		normal = k
		for n in range(3):
			objFile.write('/'.join(map(str, [face["vertices"][n], face["UVs"][n], normal])))
			if n < 2:
				objFile.write(' ')
		objFile.write('\n')
	objFile.close()
	print("File created!")

jsonDumpFile = open("icosaUVGenDump.json", 'w')
jsonDumpFile.write(json.dumps(vertices, indent = 4))
jsonDumpFile.write('\n')
jsonDumpFile.write(json.dumps(triangleData, indent = 4))
jsonDumpFile.close()
