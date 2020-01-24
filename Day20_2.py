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
test2_text = \
"""             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
"""
test2 = [line.rstrip('\n') for line in test2_text.rstrip('\n').split('\n')]


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

def is_inner(rooms, coords):
	xs = [k[0] for k in rooms.keys() if type(k) == type((0,0))]
	ys = [k[1] for k in rooms.keys() if type(k) == type((0,0))]
	x = coords[0]
	y = coords[1]
	return x > 3 and y > 3 and x < max(xs) and y < max(ys)


def traverse_maze(rooms, start_name, end_name):
	seen = [[] for n in range(500)]
	room_queue = [(rooms[rooms[start_name]], -1, 0)]
	
	while True:
		(nr, steps, level) = room_queue.pop(0)
		if (nr.x,nr.y,level) in seen[level]: continue
		seen[level].append((nr.x,nr.y,level))
		
		if nr.type == RoomType.terminus and level == 0 and nr.name == end_name:
			print("Found terminus %s at (%2d,%2d) in %d steps" % (end_name, nr.x, nr.y, steps))
			return steps

		for c in [(nr.x-1,nr.y), (nr.x+1,nr.y), (nr.x,nr.y-1), (nr.x,nr.y+1)]:
			if c in rooms and c not in seen:
				r = rooms[c]
				if r.type == RoomType.open:
					room_queue.append((r, steps+1, level))
				elif r.type == RoomType.terminus and level == 0:
					room_queue.append((r, steps, level))
				elif r.type == RoomType.warp:
					if level == 0 and not is_inner(rooms, c): continue
					
					dest = get_warp_destination(rooms, c, r.name)
					dx = dest[0]
					dy = dest[1]
					dl = (level + 1) if is_inner(rooms, c) else (level - 1)
					for c2 in [(dx-1,dy), (dx+1,dy), (dx,dy-1), (dx,dy+1)]:
						if c2 in rooms and c2 not in seen:
							room_queue.append((rooms[c2], steps+1, dl))



rooms = parse_maze_text(maze_text)
steps = traverse_maze(rooms, "AA", "ZZ")
print("Part 2:", steps)

