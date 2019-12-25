import time
import copy
import os

with open('Input16.txt') as f:
	signal = [int(c) for c in next(f).strip()]


def calc_phase(sig):
	num_phases = len(sig)
	out_list = []
	dot_vect = [0,1,0,-1]
	
	for n in range(1, num_phases+1):
		dp = 0
		for s in range(n, len(sig)+1):
			idx = (i // (n)) % 4
			dp += sig[s-1] * dot_vect[idx]
		out_list.append(abs(dp) % 10)
	return out_list

def calc_phase2(sig):
	out_list = []
	for n in range(1, len(sig)+1):
		num_plusses = len(sig) // (4*n)

test1 = [1,2,3,4,5,6,7,8]
test2 = [8,0,8,7,1,2,2,4,5,8,5,9,1,4,5,4,6,6,1,9,0,8,3,2,1,8,6,4,5,5,9,5]

test1 = calc_phase(test1)
print(test1)

p1_sig = copy.deepcopy(signal)
for n in range(100):
	p1_sig = calc_phase(p1_sig)
print("Part 1: ", p1_sig[0:8])


def part2(signal):
	msg_offset = 0
	for c in range(7):
		msg_offset += signal[c] * 10**(6-c)
	sig = signal * 10000
	for n in range(100):
		sig = calc_phase(sig)
	return sig[msg_offset, msg_offset + 8]


p1_sig = signal * 10000
msg_offset = 0
for c in range(7):
	msg_offset += signal[c] * 10**(6-c)

print("Message offset: ", msg_offset)

test = [int(c) for c in "03036732577212944063491565474664"]
print("Test: ", part2(test))

print("Part 2:")
print(part2(signal))

