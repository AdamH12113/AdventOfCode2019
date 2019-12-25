import copy
import re

input = """<x=17, y=5, z=1>
<x=-2, y=-8, z=8>
<x=7, y=-6, z=14>
<x=1, y=-10, z=4>
"""

test1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

test2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""

class Body:
	def __init__(self, x0, y0, z0):
		self.x = x0
		self.y = y0
		self.z = z0
		self.vx = 0
		self.vy = 0
		self.vz = 0

	def __repr__(self):
		return "<%3d,%3d,%3d><%3d,%3d,%3d>" % (self.x,self.y,self.z,self.vx,self.vy,self.vz)

def get_coords(s):
	return [Body(int(c[0]), int(c[1]), int(c[2])) for c in (re.findall(r'[-+]?\d+', L) for L in s.splitlines())]

def get_energy(b):
	pe = abs(b.x) + abs(b.y) + abs(b.z)
	ke = abs(b.vx) + abs(b.vy) + abs(b.vz)
	return ke * pe

def sim_step(bodies):
	for body1 in bodies:
		for body2 in bodies:
			body1.vx += (body1.x < body2.x) - (body1.x > body2.x)
			body1.vy += (body1.y < body2.y) - (body1.y > body2.y)
			body1.vz += (body1.z < body2.z) - (body1.z > body2.z)

	for body in bodies:
		body.x += body.vx
		body.y += body.vy
		body.z += body.vz

	return bodies

def sim_energy(bodies, steps):
	for s in range(0, steps):
		bodies = sim_step(bodies)
	return sum([get_energy(b) for b in bodies])

coords_test = [get_coords(test1), get_coords(test2)]
in_coords = get_coords(input)

print(sim_energy(copy.deepcopy(coords_test[0]), 10))
print(sim_energy(copy.deepcopy(coords_test[1]), 100))
print("Part 1: ", sim_energy(copy.deepcopy(in_coords), 1000))


energy_set = {}
step = 0
bodies = copy.deepcopy(coords_test[1])
while True:
	energy = sum([get_energy(b) for b in bodies])
	print(bodies, energy)
	if energy == 0:
		print("Found 0 energy at step %d: " % (step), bodies)
	bodies = sim_step(bodies)
	step += 1
	if step % 10000000 == 0: print(step)
