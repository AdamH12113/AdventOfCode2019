import copy
import math
from Intcode import CPU

with open('Input21.txt') as f:
	program = next(f).strip()

sdprog1 = \
"""NOT J T
OR T J
OR J T
AND A T
AND B T
AND C T
NOT T T
AND T J
AND D J
WALK
"""

input = [ord(c) for c in sdprog1]
output = []
cpu = CPU(program, input, output)
cpu.execute()
result = output.pop() if output[-1] > 127 else -1
out_text = "".join([chr(c) for c in output])
print(out_text)
print("Part 1: ", "FAIL" if result == -1 else result)


sdprog2 = \
"""NOT J T
OR T J
OR J T
AND A T
AND B T
AND C T
NOT T T
AND T J
AND D J
NOT A T
AND A T
OR E T
OR H T
AND T J
RUN
"""

input = [ord(c) for c in sdprog2]
output = []
cpu = CPU(program, input, output)
cpu.execute()
result = output.pop() if output[-1] > 127 else -1
out_text = "".join([chr(c) for c in output])
print(out_text)
print("Part 2: ", "FAIL" if result == -1 else result)
