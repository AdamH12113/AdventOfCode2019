import copy
import math
import time
import os

with open('Input18.txt') as f:
	input_maze = [line.rstrip() for line in f]
	
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
# the process to put this in a form that makes it easy to solve the Traveling
# Salesman Problem.
class BFS_State:
	def __init__(self, x, y, steps, required):
		self.x = x
		self.y = y
		self.steps = steps
		self.required = required
		
	def __repr__(self):
		return "BFS (%2d,%2d) %3d %s" % (self.x, self.y, self.steps, "".join(self.required))

def construct_node_paths(maze, sx, sy):
	distances = {}
	next = [BFS_State(sx,sy,0,[])]
	seen = {}
	
	# We can take advantage of the fact that the maze is bounded to
	# avoid doing range checks on the x/y coordinates
	while True:
		if next == []: break
		nc = next.pop(0)
		x = nc.x
		y = nc.y
		required = copy.deepcopy(nc.required)
		if (x,y) in seen: continue
		seen[(x,y)] = 1
		type = maze[y][x]
		assert type != '#', "Walked into a wall at (%2d,%2d) queue: " % (x,y) + str(next)
		
		# Don't include the distance to the starting node. We're not constructing
		# a complete graph to reduce the TSP branching, so we can stop at each key.
		if type != '.' and type != maze[sy][sx]:
			if type in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				required += [type.lower()]
			elif type in "abcdefghijklmnopqrstuvwxyz":
				distances[type] = (nc.steps, required)
				continue

		for coords in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
			nx = coords[0]
			ny = coords[1]
			if not (nx,ny) in seen and maze[ny][nx] != '#':
				next.append(BFS_State(nx,ny,nc.steps+1, required))

	return distances

def construct_weighted_graph(maze):
	graph = {}
	
	for y in range(len(maze)):
		for x in range(len(maze[0])):
			cur = maze[y][x]
			if cur != '.' and cur != '#':
				graph[cur] = construct_node_paths(maze, x, y)
	return graph


maze = test_mazes[4]
print("Maze size (%2d,%2d)" % (len(maze[0]), len(maze)))
graph = construct_weighted_graph(maze)
all_keys = sorted([k for k in list(graph.keys()) if k.islower()])
all_doors = sorted([k for k in list(graph.keys()) if k.isupper()])
keys_subgraph = {k:graph[k] for k in all_keys}
keys_subgraph.update({'@':graph['@']})

class TSP_State:
	def __init__(self, node, steps, have, visited):
		self.node = node
		self.steps = steps
		self.have = have
		self.visited = visited

	def __repr__(self):
		return "TSP [%s -> %s] %3d %s" % (self.visited, self.node, self.steps, "".join(self.have))

def node_reachable(have, needed):
	return all([(n in have) for n in needed])

def find_shortest_collection_route(graph, full_set, start_node):
	next = [TSP_State(start_node, 0, "", '')]
	distances = [999999999]
	shortest = 999999999
	dc = 0

	while True:
		if next == []: break
		nn = next.pop(0)
		if nn.steps > shortest: continue
		
		found_key = nn.node not in nn.have
		new_have = nn.have + (nn.node if found_key else "")
		new_visited = "" if found_key else (nn.visited + nn.node)
		dc += 1
		if dc % 1000 == 0:
			print("[%16s -> %s] %3d  %16s  %s" % (nn.visited, nn.node, nn.steps, new_have, found_key))

		if node_reachable(new_have, full_set):
			print("Done with %d steps at node %s" % (nn.steps, nn.node))
			distances.append(nn.steps)
			shortest = min(distances)
			continue
		
		for new_node in graph[nn.node]:
			if new_node != '@' and new_node not in new_visited:
				new_steps = nn.steps + graph[nn.node][new_node][0]
				new_needed = graph[nn.node][new_node][1]
				if new_steps > shortest: continue
				if node_reachable(new_have, new_needed):
					new_state = TSP_State(new_node, new_steps, new_have, new_visited)
#					print("  ", new_state)
					next.append(new_state)
	
	return distances

print(keys_subgraph)
ds = find_shortest_collection_route(keys_subgraph, all_keys, '@')
print(ds)
print(min(ds))

