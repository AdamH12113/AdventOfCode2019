import copy

class CPU:
	def __init__(self, program_string, input_source, output_sink):
		self.prog = [int(i) for i in program_string.split(',')]
		self.prog += [0] * (16384 - len(self.prog))
		self.input = input_source
		self.output = output_sink
		self.ip = 0
		self.relative_base = 0
	
	def execute(self):
		isizes = [1, 4, 4, 2, 2, 3, 3, 4, 4, 2]
		prog = self.prog
		
		while True:
			# Decode the opcode and parameter modes
			ip = self.ip
			rb = self.relative_base
			op =  prog[ip] % 100
			mode1 = (prog[ip] // 100) % 10
			mode2 = (prog[ip] // 1000) % 10
			mode3 = (prog[ip] // 10000) % 10
			assert ((op >= 1 and op <= 9) or op == 99) and (mode1 >= 0 and mode1 <= 2) and \
			       (mode2 >= 0 and mode2 <= 2) and (mode3 >= 0 and mode3 <= 2), \
			       "Invalid opcode at ip %d: %d" % (ip, prog[ip])

			# Hack to include the halt instruction in the size list
			if op == 99: op = 0

			# Create "pointers" to the parameters
			if isizes[op] > 1:
				if mode1 == 0:   r1 = prog[ip + 1]
				elif mode1 == 1: r1 = ip + 1
				elif mode1 == 2: r1 = prog[ip + 1] + rb
			if isizes[op] > 2:
				if mode2 == 0:   r2 = prog[ip + 2]
				elif mode2 == 1: r2 = ip + 2
				elif mode2 == 2: r2 = prog[ip + 2] + rb
			if isizes[op] > 3:
				if mode3 == 0:   r3 = prog[ip + 3]
				elif mode3 == 1: r3 = ip + 3
				elif mode3 == 2: r3 = prog[ip + 3] + rb

			# Execute the operation
			if op == 1:
				prog[r3] = prog[r1] + prog[r2]          # Add
			elif op == 2:
				prog[r3] = prog[r1] * prog[r2]          # Multiply
			elif op == 3:
				if len(self.input) > 0:                 # Input
					next_input = self.input.pop(0)
					prog[r1] = next_input
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
			elif op == 9:
				self.relative_base += prog[r1]          # Adjust relative base
			elif op == 0:
				return True                             # Halt
			self.ip += isizes[op]
