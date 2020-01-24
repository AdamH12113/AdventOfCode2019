import time
import copy
import os
import numpy as np

with open('Input16.txt') as f:
	signal = [int(c) for c in next(f).strip()]

test1 = np.array([1,2,3,4,5,6,7,8]).reshape(8,1)
test2 = [8,0,8,7,1,2,2,4,5,8,5,9,1,4,5,4,6,6,1,9,0,8,3,2,1,8,6,4,5,5,9,5]

# Just for fun, let's use NumPy
def create_transform(N):
	base = [0, 1, 0, -1]
	matrix = np.zeros((N,N), dtype=np.int32)
	for n in range(0, N):
		for m in range(n, N):
			idx = ((m+1) // (n+1)) % len(base)
			matrix[n,m] = base[idx]
	return matrix

N = len(signal)
tr = create_transform(N)
sig = np.array(signal, dtype=np.int32, copy=True).reshape(N,1)
for n in range(100):
	np.dot(tr, sig, out=sig)
	np.absolute(sig, out=sig)
	np.mod(sig, 10, out=sig)
print("Part 1: ", sig[:8].flatten())


def get_offset(sig):
	off = 0
	for n in sig[:7]:
		off = off*10 + n
	return off

# This is humiliating, but I had to look up the solution for this. I had discovered
# this optimization, but mistakenly thought that I had to compute the whole
# transform, not realizing that my message offset is more than halfway through
# the list. The optimized version runs in linear time, which is much better than
# the naive O(n^2).
def phase2(sig, out):
	L = len(sig)
	out[L - 1] = sig[L - 1]
	for n in range(L - 2, -1, -1):
		out[n] = (sig[n] + out[n+1]) % 10

offset = get_offset(signal)
print("Message offset: ", offset)
p2_sig = signal * 10000
subset = p2_sig[offset:]
for n in range(100):
	print(n)
	phase2(subset, subset)

print("Part 2: ", subset[:8])
