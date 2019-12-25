import copy
import math
from Intcode import CPU

with open('Input19.txt') as f:
	program = next(f).strip()

points_affected = 0
for y in range(0, 50):
	for x in range(0, 50):
		input = [x, y]
		output = []
		cpu = CPU(program, input, output)
		cpu.execute()
		out = output.pop(0)
		points_affected += out
		print(out, end='')
	print()

print("Part 1: ", points_affected)

limit = 2000
size = 100
map = []
for y in range(0, limit):
	line = []
	for x in range(0, limit):
		input = [x, y]
		output = []
		cpu = CPU(program, input, output)
		cpu.execute()
		out = output.pop(0)
		line.append(out)
	map.append(line)
	print(y)

for y in range(0, limit - size):
	for x in range(0, limit - size):
		if map[y][x] == 1:
			fits = True
			for xp in range(x, x + size):
				if map[y][xp] != 1: fits = False
			for yp in range(y, y + size):
				if map[yp][x] != 1: fits = False
			if fits:
				print("Found fit at %d, %d" % (x, y))
				quit()




