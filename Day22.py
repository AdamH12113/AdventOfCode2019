import copy
import math
import re

with open('Input22.txt') as f:
	instructions = f.read()

def deal_into_new(deck):
	return list(reversed(deck))

def cutn(deck, n):
	dlen = len(deck)
	N = abs(n)
	if n > 0:
		return deck[N:] + deck[0:N]
	elif n < 0:
		return deck[dlen-N:] + deck[:dlen-N]
	else:
		raise ValueError(n)

def deal_with_increment(deck, N):
	dlen = len(deck)
	table = [-1 for n in range(dlen)]
	for n in range(dlen):
		table[(N*n) % len(deck)] = deck[n]
	return table


def shuffle(instructions, deck_len):
	deck = [n for n in range(deck_len)]
	for line in instructions.split('\n'):
		if re.match(r'deal into new stack', line) != None:
#			print("Deal new")
			deck = deal_into_new(deck)
		elif re.match(r'deal with increment', line) != None:
			inc = int(line.split(' ')[-1])
#			print("Deal inc ", inc)
			deck = deal_with_increment(deck, inc)
		elif re.match(r'cut', line) != None:
			N = int(line.split(' ')[-1])
#			print ("Cut ", N)
			deck = cutn(deck, N)
	return deck


tin1 = """deal with increment 7
deal into new stack
deal into new stack
"""
tin2 = """cut 6
deal with increment 7
deal into new stack
"""
tin3 = """deal with increment 7
deal with increment 9
cut -2
"""
tin4 = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""

out = shuffle(tin3, 10)
print(out, "\n")


out = shuffle(tin4, 10)
print(out)

print(instructions)
out = shuffle(instructions, 10007)
print("Part 1: ", out.index(2019))






