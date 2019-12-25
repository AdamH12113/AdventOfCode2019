import copy
import math
from Intcode import CPU

with open('Input15.txt') as f:
	program = next(f).strip()


def update_coord(coord, dir):
	if dir == 1:
		return (coord[0], coord[1] + 1)
	elif dir == 2:
		return (coord[0], coord[1] - 1)
	elif dir == 3:
		return (coord[0] - 1, coord[1])
	elif dir == 4:
		return (coord[0] + 1, coord[1])
	else:
		raise ValueException("Bad direction %d for (%d,%d)" % (dir, coord[0], coord[1]))

def bfs(cpu):
	start = (0,0)
	explored = {start: 1}
	cpu.coord = start
	cpu.moves = 0
	last_cpu = cpu
	next_queue = [cpu]
	
	while True:
		cur_cpu = next_queue.pop(0)
		for dir in range(1, 4+1):
			if update_coord(cur_cpu.coord, dir) in explored:
				continue

			new_cpu = copy.deepcopy(cur_cpu)
			new_cpu.input = [dir]
			new_cpu.output = []
			new_cpu.execute()
			new_cpu.coord = update_coord(new_cpu.coord, dir)
			explored[new_cpu.coord] = new_cpu.output[0]
			new_cpu.moves += 1

			if new_cpu.moves > last_cpu.moves:
				last_cpu = copy.deepcopy(new_cpu)
			
			if new_cpu.output[0] == 0:
				continue
			elif new_cpu.output[0] == 1:
				next_queue.append(new_cpu)
			elif new_cpu.output[0] == 2:
				print("Found oxygen system at (%3d,%3d) in %d moves" % (new_cpu.coord[0], new_cpu.coord[1], new_cpu.moves))
				explored = {new_cpu.coord: 2}
				new_cpu.moves = 0
				last_cpu.moves = 0
				next_queue = [new_cpu]
				print("Searching for the farthest step...", len(next_queue), len(explored))
				break
			else:
				raise ValueException("Bad output %d" % (new_cpu.output[0]))

		if next_queue == []:
			print("Found farthest step at (%3d,%3d) in %d moves" % (last_cpu.coord[0], last_cpu.coord[1], last_cpu.moves))
			return


cpu = CPU(program, [], [])
print("Parts 1 and 2:")
final = bfs(cpu)


