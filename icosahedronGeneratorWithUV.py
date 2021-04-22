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
				t = tuple(sorted([n, m, k]))
				if t not in triangles:
					triangles.append(t)
				else:
					continue
			else:
				continue
for t in triangles:
	print(triangles.index(t), ':', t)
# Generate 20 normal vectors for the faces
triangleData = {}
neededCrossProdRedo = []
for t in triangles:
	# Get two edges of the triangle
	e1 = vecDiff(vertices[t[1]], vertices[t[0]])
	e2 = vecDiff(vertices[t[2]], vertices[t[0]])
	# Calculate the normal
	n = normalize(crossProd(e1, e2))
	# Check if the normal is pointing the right way
	if vecAngle(n, vertices[t[0]]) > 90.0:
		# Fix the normal if its pointing the wrong way
		n = normalize(crossProd(e2, e1))
		# Mark the triangle for fixing later
		neededCrossProdRedo.append(triangles.index(t))
	triangleData[triangles.index(t)] = { \
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
aboveFaces = (0, 2, 4, 5, 7, 12, 13, 14, 15, 18)
aboveUVVertices = {n for n in range(11)}
belowFaces = (1, 3, 6, 8, 9, 10, 11, 16, 17, 19)
belowUVVertices = {n for n in range(11, 24)}

leftFaces = (0, 5, 8, 9, 13, 16, 17, 18, 19)
leftUVVertices = {n for n in range(5, 18)}
rightFaces = (1, 2, 3, 4, 6, 10, 11, 14, 15)
rightUVVertices = {n for n in range(6)} | {n for n in range(17, 24)}
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
	{2, 10, 19}, {9, 18}, {3, 8, 11, 12}, {20},
	{5, 21}, {1, 17}, {5, 13}, {4, 17},
	{0, 8, 22, 23}, {14}, {6, 16}, {2, 7, 15}
]
upUVVertices = [8, 20, 4, 21, 4, 5, 17, 5, 11, 12, 23, 22, 5, 5, 1, 1, 13, 17, 8, 14]
# Derive ordered UV vertices for every face
for face in triangleData.keys():
	realVertices = triangleData[face]["vertices"]
	# perform a Set Union to start
	possibleUVVertices = \
		realToUV[realVertices[0]] | realToUV[realVertices[1]] | realToUV[realVertices[2]]
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
	if face in (8, 11): # Lefthand faces (thus the actual vertices have locally low u values)
		possibleUVVertices = possibleUVVertices - {
			max(possibleUVVertices, key = lambda v : verticesUV[v][0])
		}
	elif face in (9, 10): # Righthand faces (thus the actual vertices have locally high u values)
		possibleUVVertices = possibleUVVertices - {
			min(possibleUVVertices, key = lambda v : verticesUV[v][0])
		}

	print("Filtered Full", format(str(possibleUVVertices), " <16s"), end = ";\n")
	# By here only 3 UV vertices remain, exactly enough;
	# They need to be in the same order as the real vertices though,
	# but it is known what real vertices correspond to which UV vertices,
	# so do an intersection per real vertex and use the sole element
	orderedUVs = [
		tuple(possibleUVVertices.intersection(realToUV[r]))[0]
		for r in realVertices
	]
	# Swap the two vertices that make an underline for the number (if this were a d20)
	# Otherwise the textures will appear mirrored
	topVertexIndex = orderedUVs.index(upUVVertices[face])
	swapIndices = list({0, 1, 2} - {topVertexIndex})
	i = swapIndices[0]
	j = swapIndices[1]
	temp = orderedUVs[i]
	orderedUVs[i] = orderedUVs[j]
	orderedUVs[j] = temp

	print("Real Vertices:", format(str(realVertices), " <20s"), end = "; ")
	print("Ordered UV Vertices:", format(str(orderedUVs), " <20s"))

	triangleData[face]["UVs"] = orderedUVs

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
	#s = 1
	for v in verticesUV:
		#print(s, v)
		#s += 1
		objFile.write("vt " + ' '.join(map(str, v)) + '\n')
	for k in range(20):
		objFile.write("vn ")
		s = 0
		for c in triangleData[k]["normal"]:
			objFile.write(str(c))
			if s < 2:
				objFile.write(' ')
			s += 1
		objFile.write('\n')
	for k in range(20):
		objFile.write("f ")
		face = triangleData[k]
		normal = k + 1
		for n in range(3):
			objFile.write('/'.join(map(str, [face["vertices"][n] + 1, face["UVs"][n] + 1, normal])))
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
