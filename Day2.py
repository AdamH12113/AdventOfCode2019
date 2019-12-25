import copy

with open('input7.txt') as f:
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

		if op == 1:
			prog[ad] = prog[as1] + prog[as2]
		elif op == 2:
			prog[ad] = prog[as1] * prog[as2]
			ip += 4
	return prog

test_progs = [[1,9,10,3,2,3,11,0,99,30,40,50], [1,0,0,0,99], [2,3,0,3,99], [2,4,4,5,99,0], [1,1,1,4,99,5,6,0,99]]
for p in test_progs:
	print("Program: ", p)
	print("Becomes: ", run_program(p), "\n")

part1_prog = copy.deepcopy(program)
part1_prog[1] = 12
part1_prog[2] = 2
print("Part 1 answer: ", run_program(part1_prog)[0], "\n")


for n in range(0, 99):
	for v in range(0, 99):
		nv_prog = copy.deepcopy(program)
		nv_prog[1] = n
		nv_prog[2] = v
		try:
			nv_prog = run_program(nv_prog)
		except:
			continue
		if nv_prog[0] == 19690720:
			print("Answer %d found with noun=%d, verb=%d" % (100*n + v, n, v))
			exit(0)

print("Failed to find an answer for part 2")
