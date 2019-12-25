import copy
import itertools
from enum import Enum

with open('Input7.txt') as f:
	program = [int(i) for i in next(f).split(',')]


class CPU:
	def __init__(self, program, input_source, output_sink):
		self.prog = copy.deepcopy(program)
		self.input = input_source
		self.output = output_sink
		self.ip = 0
	
	def execute(self):
		isizes = [1, 4, 4, 2, 2, 3, 3, 4, 4]
		prog = self.prog
		
		while True:
			# Decode the opcode and parameter modes
			ip = self.ip
			op =  prog[ip] % 100
			mode1 = (prog[ip] // 100) % 10
			mode2 = (prog[ip] // 1000) % 10
			mode3 = (prog[ip] // 10000) % 10
			assert ((op >= 1 and op <= 8) or op == 99) and (mode1 == 0 or mode1 == 1) and \
			       (mode2 == 0 or mode2 == 1) and (mode3 == 0 or mode3 == 1), \
			       "Invalid opcode at ip %d: %d" % (ip, prog[ip])

			# Hack to include the halt instruction in the size list
			if op == 99: op = 0

			# Create "pointers" to the parameters
			if isizes[op] > 1:
				r1 = (ip + 1) if mode1 == 1 else prog[ip + 1]
			if isizes[op] > 2:
				r2 = (ip + 2) if mode2 == 1 else prog[ip + 2]
			if isizes[op] > 3:
				r3 = (ip + 3) if mode3 == 1 else prog[ip + 3]

			# Execute the operation
			if op == 1:
				prog[r3] = prog[r1] + prog[r2]          # Add
			elif op == 2:
				prog[r3] = prog[r1] * prog[r2]          # Multiply
			elif op == 3:
				if len(self.input) > 0:                 # Input
					prog[r1] = self.input.pop(0)
				else:
					return False
			elif op == 4:
				self.output.append(prog[r1])            # Output
			elif op == 5:
				if prog[r1] != 0:                       # BNZ
					self.ip = prog[r2]
					continue
			elif op == 6:
				if prog[r1] == 0:                       # BZ
					self.ip = prog[r2]
					continue
			elif op == 7:
				prog[r3] = int(prog[r1] < prog[r2])     # LE
			elif op == 8:
				prog[r3] = int(prog[r1] == prog[r2])    # EQ
			elif op == 0:
				return True                             # Halt
			self.ip += isizes[op]
			

def run_one_amplifier(program, phase, input):
	inputs = [phase, input]
	outputs = []
	amp = CPU(program, inputs, outputs)
	amp.execute()
	return outputs


def run_amplifiers(program, phases):
	a = run_one_amplifier(program, phases[0], 0).pop(0)
	b = run_one_amplifier(program, phases[1], a).pop(0)
	c = run_one_amplifier(program, phases[2], b).pop(0)
	d = run_one_amplifier(program, phases[3], c).pop(0)
	e = run_one_amplifier(program, phases[4], d).pop(0)
	return e

def find_max_phases(program, phase_set, func=run_amplifiers):
	phase_groups = itertools.permutations(phase_set)
	max_output = -1
	max_phases = []
	
	for pg in phase_groups:
		phases = list(pg)
		output = func(program, phases)
		if output > max_output:
			max_output = output
			max_phases = phases
	print("Max output %d for phases " % max_output, max_phases)


test_progs1 = [[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]]

p1_phase_set = [0,1,2,3,4]
find_max_phases(test_progs1[0], p1_phase_set)
find_max_phases(test_progs1[1], p1_phase_set)
find_max_phases(test_progs1[2], p1_phase_set)

print("Part 1: ", end='')
find_max_phases(program, p1_phase_set)


def run_feedback_amplifiers(program, phases):
	in_a = [phases[0], 0]
	in_b = [phases[1]]
	in_c = [phases[2]]
	in_d = [phases[3]]
	in_e = [phases[4]]
	
	a = CPU(program, in_a, in_b)
	b = CPU(program, in_b, in_c)
	c = CPU(program, in_c, in_d)
	d = CPU(program, in_d, in_e)
	e = CPU(program, in_e, in_a)
	
	# Round robin scheduling
	while True:
		af = a.execute()
		bf = b.execute()
		cf = c.execute()
		df = d.execute()
		ef = e.execute()
		
		if af and bf and cf and df and ef:
			return in_a.pop(0)

test_progs2 = [[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]]

p2_phase_set = [5,6,7,8,9]
find_max_phases(test_progs2[0], p2_phase_set, func=run_feedback_amplifiers)
find_max_phases(test_progs2[1], p2_phase_set, func=run_feedback_amplifiers)

print("Part 2: ", end='')
find_max_phases(program, p2_phase_set, func=run_feedback_amplifiers)
