import copy
import math
import time
import os
import numpy as np

# Apparently this only takes twice as long as the optimal bitmask-based algorithm. (!!)
# An intrinsic function might be added to Python 3.9. Strange how poorly-supported
# this is in many languages given that modern CPUs have an instruction for it.
def popcount(x):
	return bin(x).count("1")

input = \
"""##.#.
##.#.
##.##
.####
.#...
"""

test = \
"""....#
#..#.
#..##
..#..
#....
"""

class Grid:
	# We can use 64-bit values here, so the center point for comparison is
	# shifted out of the 25-bit data range
	grid_size = 5*5
	mc = 50
	adj_mask_center = 1<<(mc + 1) | 1<<(mc - 1) | 1<<(mc + 5) | 1<<(mc - 5)
	adj_mask_left = 1<<(mc + 1) | 1<<(mc + 5) | 1<<(mc - 5)
	adj_mask_right = 1<<(mc - 1) | 1<<(mc + 5) | 1<<(mc - 5)
	range_mask = (1 << grid_size) - 1

	def __init__(self, text_state):
		s = "".join(text_state.split('\n'))
		bs = "".join(list(reversed(["1" if c == "#" else "0" for c in s])))
		self.state = int(bs, 2)
	
	def __repr__(self):
		bin_str = bin(self.state + (1 << self.grid_size))[3:]
		s = "".join(["#" if b == "1" else "." for b in reversed(bin_str)])
		snl = "\n".join(s[i:i+5] for i in range(0, len(s)+1, 5))
		return snl
	
	def __index__(self):
		return self.state

	def evolve(self):
		cur_state = self.state
		new_state = 0
		mc = self.mc
		
		for n in range(0, self.grid_size):
			set = (cur_state >> n) & 0x1
			shifted = cur_state << (mc - n)
			am = self.adj_mask_left if n % 5 == 0 else self.adj_mask_right if n % 5 == 4 else self.adj_mask_center
			adj_bits = popcount(shifted & am)
			if (set and adj_bits == 1) or (not set and (adj_bits == 1 or adj_bits == 2)):
				new_state |= 1 << n
		self.state = new_state

grid = Grid(input)
seen = {grid.state: 1}
while True:
	grid.evolve()
	if grid.state in seen:
		print("Part 1: ", grid.state)
		break
	else:
		seen[grid.state] = 1


# Well, that was fun, but part 2 is totally different. :-(
def recursive_evolve(map):
	adjmap = np.zeros_like(map)
	
	for d in range(1, 398):
		for x in range(5):
			for y in range(5):
				if x == 2 and y == 2: continue
				adj = 0
				
				# Left tile
				if x == 0:
					adj += map[d-1, 1, 2]
				elif x == 3 and y == 2:
					adj += sum(map[d+1, 4, :])
				else:
					adj += map[d, x-1, y]

				# Right tile
				if x == 4:
					adj += map[d-1, 3, 2]
				elif x == 1 and y == 2:
					adj += sum(map[d+1, 0, :])
				else:
					adj += map[d, x+1, y]

				# Top tile
				if y == 0:
					adj += map[d-1, 2, 1]
				elif x == 2 and y == 3:
					adj += sum(map[d+1, :, 4])
				else:
					adj += map[d, x, y-1]
				
				# Bottom tile
				if y == 4:
					adj += map[d-1, 2, 3]
				elif x == 2 and y == 1:
					adj += sum(map[d+1, :, 0])
				else:
					adj += map[d, x, y+1]
				
				adjmap[d,x,y] = adj
	
	for d in range(1, 398):
		for x in range(5):
			for y in range(5):
				if x == 2 and y== 2: continue
				
				if map[d,x,y] == 1 and adjmap[d,x,y] != 1:
					map[d,x,y] = 0
				elif map[d,x,y] == 0 and (adjmap[d,x,y] == 1 or adjmap[d,x,y] == 2):
					map[d,x,y] = 1
	return adjmap

basemap = np.zeros((400,5,5), dtype=np.int32)
ingrid = np.array([[1,1,0,1,0],
                   [1,1,0,1,0],
		           [1,1,0,1,1],
		           [0,1,1,1,1],
		           [0,1,0,0,0]], dtype=np.int32).transpose()

testgrid = np.array([[0,0,0,0,1],
                     [1,0,0,1,0],
			         [1,0,0,1,1],
			         [0,0,1,0,0],
			         [1,0,0,0,0]], dtype=np.int32).transpose()

def printgrid(map, d):
	for y in range(5):
		for x in range(5):
			if x == 2 and y == 2: print("*", end='')
			elif map[d,x,y] == 0: print("-", end='')
			else: print(map[d,x,y], end='')
		print()

basemap[200] = ingrid

for n in range(200):
	recursive_evolve(basemap)

for d in range(199, 201+1):
	printgrid(basemap, d)
	print()

print("Part 2: ", sum(sum(sum(basemap))))

quit()
