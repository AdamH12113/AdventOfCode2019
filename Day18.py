import copy
import math
import time
import os

with open('Input18.txt') as f:
	maze = [line.rstrip() for line in f]
	
test_mazes = [ \
"""#########
#b.A.@.a#
#########
""".rstrip().split('\n'),
"""########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""".rstrip().split('\n'),
"""########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""".rstrip().split('\n'),
"""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
""".rstrip().split('\n'),
"""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
""".rstrip().split('\n') ]



# This is a nightmare. We have to do breadth-first searches to figure out the
# shortest paths between each pair of nodes, constructing a weighted digraph in
# the processto put this in a form that makes it easy to solve the Traveling
# Salesman Problem.
class BFS_State:
	def __init__(self, x, y, steps):
		self.x = x
		self.y = y
		self.steps = steps
		
	def __repr__(self):
		return "BFS (%2d,%2d) %3d" % (self.x, self.y, self.steps)

def construct_node_paths(maze, sx, sy):
	distances = {}
	next = [BFS_State(sx,sy,0)]
	seen = {}
	
	# We can take advantage of the fact that the maze is bounded to
	# avoid doing range checks on the x/y coordinates
	while True:
		if next == []: break
		nc = next.pop(0)
		x = nc.x
		y = nc.y
		if (x,y) in seen: continue
		seen[(x,y)] = 1
		type = maze[y][x]
		assert type != '#', "Walked into a wall at (%2d,%2d) queue: " % (x,y) + str(next)
		
		# Don't include the distance to the starting node. We're not constructing
		# a complete graph since doors complicate things, so we can stop at each
		# key and door.
		if type != '.' and type != maze[sy][sx]:
			distances[type] = nc.steps
		else:		
			for coords in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
				nx = coords[0]
				ny = coords[1]
				if not (nx,ny) in seen and maze[ny][nx] != '#':
					next.append(BFS_State(nx,ny,nc.steps+1))

	return distances

def construct_weighted_graph(maze):
	graph = {}
	
	for y in range(len(maze)):
		for x in range(len(maze[0])):
			cur = maze[y][x]
			if cur != '.' and cur != '#':
				graph[cur] = construct_node_paths(maze, x, y)
	return graph

print("Maze size (%2d,%2d)" % (len(maze[0]), len(maze)))
d = construct_weighted_graph(maze)
print(d)




















