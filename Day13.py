import time
import os
from Intcode import CPU

with open('Input13.txt') as f:
	program = next(f)

input = []
output = []
game = CPU(program, input, output)
game.execute()

o = iter(output)
print("Part 1: ", sum([1 for t in list(zip(o, o, o)) if t[2] == 2]))

def output_to_tiles(output):
	tiles = {}
	while output != []:
		x = output.pop(0)
		y = output.pop(0)
		id = output.pop(0)
		tiles[(x,y)] = id
	return tiles

def draw_screen(tiles, screen):
	for (x,y) in tiles:
		id = tiles[(x,y)]
		if x == -1 and y == 0:
			screen[0] = screen[0][:43] + list("%7d" % id)
		else:
			screen[y][x] = " |#_O"[id]
	
	for y in range(0, len(screen)):
		print("".join(screen[y]))

input = []
program = "2" + program[1:]
output = []
game = CPU(program, input, output)
screen = [list(" ") * 43 for y in range(0, 25+1)]

joystick = [0,0,0,1,1,1,1,1,1,1,1,1,1] + [1]*10000
ball = -1
paddle = -1

while True:
	done = game.execute()
	tiles = output_to_tiles(output)
	inv_tiles = {v:k for k,v in tiles.items()}
	_ = os.system("cls")
	draw_screen(tiles, screen)
#	print("Ball ", inv_tiles[4])
	if 4 in inv_tiles:
		ball = inv_tiles[4][0]
	if 3 in inv_tiles:
		paddle = inv_tiles[3][0]
	if ball > paddle: next = 1
	elif ball < paddle: next = -1
	else: next = 0
	input.append(next)
	if done: break
