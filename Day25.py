import copy
import math
import time
import os
import sys
from Intcode import CPU

with open('Input25.txt') as f:
	program = next(f).strip()

start_input = \
"""
east
take loom
east
take fixed point
north
take spool of cat6
west
take shell
east
south
west
south
take ornament
west
north
take candy cane
south
east
north
west
north
take wreath
north
east
"""

input = [ord(c) for c in start_input]
output = []
cpu = CPU(program, input, output)

print("Running...")
while True:
	done = cpu.execute()

	if len(output) > 0:
		print("".join([chr(c) for c in output]))

	if done:
		break

	try:
		line = sys.stdin.readline()
		if line == "quit\n": quit()
		cpu.input = [ord(c) for c in line]
	except KeyboardInterrupt:
		continue


print("Execution complete")
