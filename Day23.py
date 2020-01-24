import copy
import math
from Intcode import CPU

with open('Input23.txt') as f:
	program = next(f).strip()


class Packet:
	def __init__(self, a, x, y):
		self.a = a
		self.x = y
		self.y = y


inputs = [[n] for n in range(50)]
outputs = [[] for n in range(50)]
cpus = [CPU(program, inputs[n], outputs[n]) for n in range(50)]
natx = -1
naty = -1

while True:
	for n in range(50):
		cpus[n].execute()
		inputs[n].append(-1)

		while len(outputs[n]) > 0:
			a = outputs[n].pop(0)
			x = outputs[n].pop(0)
			y = outputs[n].pop(0)

			if a == 255:
				print("Packet sent to address 255:", x, y)
				natx = x
				naty = y
			else:
				inputs[a].append(x)
				inputs[a].append(y)
	
	output_pending = sum([len(o) for o in outputs])
	input_pending = sum([len([p for p in i if p != -1]) for i in inputs])
	if output_pending == 0 and input_pending == 0:
		inputs[0].append(natx)
		inputs[0].append(naty)
		print("NAT", natx, naty)

