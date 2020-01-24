import copy
import math
import time
import os
from enum import Enum, unique

with open('Input20.txt') as f:
	maze_text = [line.rstrip('\n') for line in f]

caps = "".join([chr(c) for c in range(ord('A'), ord('Z')+1)])


test1_text = \
"""         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""
test1 = [line.rstrip('\n') for line in test1_text.rstrip('\n').split('\n')]


@unique
class RoomType(Enum):
	open = 0
	wall = 1
	warp = 2
	terminus = 3

class Room:
	def __init__(self, x, y, type, name=""):
		self.x = x
		self.y = y
		self.type = type
		self.name = name

	def __repr__(self):
		return "%s(%2d,%2d)%s" % (self.type.name, self.x, self.y, self.name)

def parse_maze_text(m):
	xr = len(m[0])
	yr = len(m)
	rooms = {}
	
	for y in range(yr):
		for x in range(xr):
			c = m[y][x]
			if c == '.':
				rooms[(x,y)] = Room(x, y, RoomType.open)
			elif c == '#':
				rooms[(x,y)] = Room(x, y, RoomType.wall)
			elif c in caps and y > 0 and y < yr-1 and x > 0 and x < xr-1:
				if m[y-1][x] in caps and m[y+1][x] == '.':
					warp_name = m[y-1][x] + c
				elif m[y+1][x] in caps and m[y-1][x] == '.':
					warp_name = c + m[y+1][x]
				elif m[y][x-1] in caps and m[y][x+1] == ".":
					warp_name = m[y][x-1] + c
				elif m[y][x+1] in caps and m[y][x-1] == '.':
					warp_name = c + m[y][x+1]
				else:
					continue

				if warp_name == "AA" or warp_name == "ZZ":
					rooms[(x,y)] = Room(x, y, RoomType.terminus, warp_name)
					rooms[warp_name] = (x,y)
				else:
					rooms[(x,y)] = Room(x, y, RoomType.warp, warp_name)
					if warp_name in rooms:
						rooms[warp_name].append((x,y))
					else:
						rooms[warp_name] = [(x,y)]

	return rooms


def get_warp_destination(rooms, coords, warp_name):
	endpoints = rooms[warp_name]
	return endpoints[1] if endpoints[0] == coords else endpoints[0]


def traverse_maze(rooms, start_name, end_name):
	seen = []
	room_queue = [(rooms[rooms[start_name]], -1)]
	
	while True:
		(nr, steps) = room_queue.pop(0)
		if nr in seen: continue
		seen.append((nr.x,nr.y))
		
		if nr.type == RoomType.terminus:
			if nr.name == end_name:
				print("Found terminus %s at (%2d,%2d) in %d steps" % (end_name, nr.x, nr.y, steps))
				return steps

		for c in [(nr.x-1,nr.y), (nr.x+1,nr.y), (nr.x,nr.y-1), (nr.x,nr.y+1)]:
			if c in rooms and c not in seen:
				r = rooms[c]
				if r.type == RoomType.open:
					room_queue.append((r, steps+1))
				elif r.type == RoomType.terminus:
					room_queue.append((r, steps))
				elif r.type == RoomType.warp:
					dest = get_warp_destination(rooms, c, r.name)
					dx = dest[0]
					dy = dest[1]
					for c2 in [(dx-1,dy), (dx+1,dy), (dx,dy-1), (dx,dy+1)]:
						if c2 in rooms and c2 not in seen:
							room_queue.append((rooms[c2], steps+1))


rooms = parse_maze_text(maze_text)
steps = traverse_maze(rooms, "AA", "ZZ")
print("Part 1:", steps)

