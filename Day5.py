import copy

with open('Input5.txt') as f:
	program = [int(i) for i in next(f).split(',')]


def run_program(prog, input):
	ip = 0
	output = -1
	isizes = [0, 4, 4, 2, 2, 3, 3, 4, 4]

	while prog[ip] != 99:
		# Decode the opcode and parameter modes
		op =  prog[ip] % 10
		mode1 = (prog[ip] // 100) % 10
		mode2 = (prog[ip] // 1000) % 10
		mode3 = (prog[ip] // 10000) % 10
		assert op >= 1 and op <= 8 and (mode1 == 0 or mode1 == 1) and (mode2 == 0 or mode2 == 1) and \
		       (mode3 == 0 or mode3 == 1), "Invalid opcode at ip %d: %d" % (ip, prog[ip])

		# Create "pointers" to the parameters
		r1 = (ip + 1) if mode1 == 1 else prog[ip + 1]
		if isizes[op] > 2:
			r2 = (ip + 2) if mode2 == 1 else prog[ip + 2]
		if isizes[op] > 3:
			r3 = (ip + 3) if mode3 == 1 else prog[ip + 3]

		# Execute the operation
		if op == 1:
			prog[r3] = prog[r1] + prog[r2]
		elif op == 2:
			prog[r3] = prog[r1] * prog[r2]
		elif op == 3:
			prog[r1] = input
		elif op == 4:
			print("Output: %d" % prog[r1])
		elif op == 5:
			if prog[r1] != 0:
				ip = prog[r2]
				continue
		elif op == 6:
			if prog[r1] == 0:
				ip = prog[r2]
				continue
		elif op == 7:
			prog[r3] = int(prog[r1] < prog[r2])
		elif op == 8:
			prog[r3] = int(prog[r1] == prog[r2])
		ip += isizes[op]
	return prog

test_prog = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
print("Tests:")
run_program(test_prog, 7)
run_program(test_prog, 8)
run_program(test_prog, 9)

part1_prog = copy.deepcopy(program)
print("\nPart 1:")
run_program(part1_prog, 1)

part2_prog = copy.deepcopy(program)
print("\nPart 2:")
run_program(part2_prog, 5)
