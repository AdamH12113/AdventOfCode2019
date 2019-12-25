import sys
import copy
import math

def read_input(file):
	with open(file) as f:
		lines = [L.strip() for L in list(f)]
		xsize = len(lines[0])
		ysize = len(lines)
		coords = []
		for x in range(0, xsize):
			for y in range(0, ysize):
				if lines[y][x] == '#':
					coords.append((x,y))
		return coords

def get_max_viewable(coords):
	max_viewable = -1
	best_asteroid = (-1,-1)
	best_deltas = {}
	for c in coords:
		deltas = {}
		for d in coords:
			if c[0] == d[0] and c[1] == d[1]:
				continue
			# Note that the coordinates go from the top left
			angle = math.atan2(c[1] - d[1], d[0] - c[0])
			dist = math.sqrt((d[0] - c[0])**2 + (d[1] - c[1])**2)
			if not angle in deltas:
				deltas[angle] = []
			deltas[angle].append((d, dist))
		if len(deltas) > max_viewable:
			max_viewable = len(deltas)
			best_asteroid = c
			best_deltas = copy.deepcopy(deltas)
	return (max_viewable, best_asteroid, best_deltas)

test = {}
for L in "abcdef":
	test[L] = read_input("Test10" + L + ".txt")
	(num, best, deltas) = get_max_viewable(test[L])
	print("Test " + L + ": (%2d,%2d) %3d" % (best[0], best[1], num))

field = read_input("Input10.txt")
(num, best, deltas) = get_max_viewable(field)
print("Part 1: (%2d,%2d) %3d" % (best[0], best[1], num))

def convert_angle(a):
	a = (a - 2*math.pi) if a > math.pi/2 else a
	return -a

def destroy_asteroids(deltas):
	for k in deltas:
		list.sort(deltas[k], key = lambda x: x[1])

	asteroid_num = 0
	while deltas != {}:
		keys = list(deltas.keys())
		list.sort(keys, key=convert_angle)
		
		for k in keys:
			try:
				coord = deltas[k].pop(0)[0]
			except:
				print(k, deltas)
				quit()
			asteroid_num += 1
			print("%3d (%2d,%2d)" % (asteroid_num, coord[0], coord[1]))
			if deltas[k] == []:
				del deltas[k]

print("Part 2:")
destroy_asteroids(deltas)





