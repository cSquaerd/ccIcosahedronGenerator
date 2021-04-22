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
# Show all the triangle data, which is vertices and normals
for n in triangleData.keys():
	print( \
		n, ':', \
		"vertices:", triangleData[n]["vertices"], \
		"; normal:", triangleData[n]["normal"] \
	)
# Prompt to and possibly write out an obj 3D model file
if input("Write a new .obj file? [Y/n]: ").upper() == 'Y':
	objFile = open("ccIcosahedron.obj", 'w')
	for v in vertices:
		objFile.write("v ")
		s = 0
		for c in v:
			objFile.write(str(c))
			if s < 2:
				objFile.write(' ')
			s += 1
		objFile.write('\n')
	objFile.write("vt 0.0 0.0\nvt 0.5 1.0\nvt 1.0 0.0\n")
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
		s = 0
		for c in triangleData[k]["vertices"]:
			objFile.write(str(c + 1) + '/' + str(s + 1) + '/' + str(k + 1))
			if s < 2:
				objFile.write(' ')
			s += 1
		objFile.write('\n')
	objFile.close()
	print("File created!")

jsonDumpFile = open("icosaGenDump.json", 'w')
jsonDumpFile.write(json.dumps(vertices, indent = 4))
jsonDumpFile.write('\n')
jsonDumpFile.write(json.dumps(triangleData, indent = 4))
jsonDumpFile.close()
