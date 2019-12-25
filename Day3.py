import copy

with open('input3.txt') as f:
	dirs1 = next(f).split(',')
	dirs2 = next(f).split(',')

def dir_to_step(dir):
	d = dir[0]
	n = int(dir[1:])
	base_dir = (1 if d == 'R' else (-1 if d == 'L' else 0), 1 if d == 'U' else (-1 if d == 'D' else 0))
	return tuple(bd * n for bd in base_dir)

def steps_to_lines(start_coord, dist, steps):
	if steps == []:
		return []
	s = steps[0]
	end_coord = tuple(s + d for s,d in zip(start_coord, s))
	new_dist = dist + abs(s[0]) + abs(s[1])
	return [(start_coord, end_coord, dist)] + steps_to_lines(end_coord, new_dist, steps[1:])

#esteps1 = [dir_to_step(s) for s in "R8,U5,L5,D3".split(',')]
#esteps2 = [dir_to_step(s) for s in "U7,R6,D4,L4".split(',')]
#esteps1 = [dir_to_step(s) for s in "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(',')]
#esteps2 = [dir_to_step(s) for s in "U62,R66,U55,R34,D71,R55,D58,R83".split(',')]
esteps1 = [dir_to_step(s) for s in "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(',')]
esteps2 = [dir_to_step(s) for s in "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(',')]

steps1 = [dir_to_step(s) for s in dirs1]
steps2 = [dir_to_step(s) for s in dirs2]

lines1 = steps_to_lines((0,0), 0, steps1)
lines2 = steps_to_lines((0,0), 0, steps2)

grid_dists = []
wire_dists = []

for seg1 in lines1:
	for seg2 in lines2:
		((xs1, ys1), (xe1, ye1), wire_dist1) = seg1
		((xs2, ys2), (xe2, ye2), wire_dist2) = seg2

		# Skip the starting intersection and parallel lines
		if wire_dist1 == 0 or wire_dist2 == 0 or (xs1 == xe1 and xs2 == xe2) or (ys1 == ye1 and ys2 == ye2):
			continue

		# Before swizzling the coordinates, do the calculations that need the original values
		xi = xs1 if xs1 == xe1 else xs2
		yi = ys1 if ys1 == ye1 else ys2
		grid_dist = abs(xi) + abs(yi)
		wire_dist1 += abs(xi - xs1) + abs(yi - ys1)
		wire_dist2 += abs(xi - xs2) + abs(yi - ys2)
		wire_dist = wire_dist1 + wire_dist2

		# Direction doesn't matter for intersections, so let's simplify to avoid
		# needing eight conditions instead of two.
		if xe1 < xs1: (xs1, xe1) = (xe1, xs1)
		if ye1 < ys1: (ys1, ye1) = (ye1, ys1)
		if xe2 < xs2: (xs2, xe2) = (xe2, xs2)
		if ye2 < ys2: (ys2, ye2) = (ye2, ys2)

		if (xs1 <= xs2 and xs2 <= xe1 and ys2 <= ys1 and ys1 <= ye2) or \
		  (xs2 <= xs1 and xs1 <= xe2 and ys1 <= ys2 and ys2 <= ye1):
			print("(%4d,%4d)-(%4d,%4d) %4d  (%4d,%4d)-(%4d,%4d) %4d " % (xs1,ys1,xe1,ye1,wire_dist1,xs2,ys2,xe2,ye2,wire_dist2), end=' ')
			print("Int (%4d,%4d) %4d %4d" % (xi,yi,grid_dist, wire_dist))
			grid_dists.append(grid_dist)
			wire_dists.append(wire_dist)

print("Part 1 answer: ", min(grid_dists))
print("Part 2 answer: ", min(wire_dists))