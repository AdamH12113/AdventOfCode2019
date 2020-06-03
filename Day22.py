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

def shuffle_one_card(instructions, deck_len, card):
	for line in instructions.rstrip().split('\n'):
#		print(card, " ", end='')
		if re.match(r'deal into new stack', line) != None:
			card = (deck_len - 1) - card
#			print("stack -> ", card)
		elif re.match(r'deal with increment', line) != None:
			inc = int(line.split(' ')[-1])
			card = (card * inc) % deck_len
#			print("inc ", inc, " -> ", card)
		elif re.match(r'cut', line) != None:
			N = int(line.split(' ')[-1])
#			print("cut ", N, " -> ", end='')
			if N < 0: N = deck_len + N
			if N >= 0:
				if card < N: card += deck_len - N
				else:        card -= N
#			print(card)
	return card

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

out = shuffle_one_card(instructions, 10007, 2019)
print("Part 1: ", out)


# Now we need to invert the transformations
def invert_shuffle(instructions, deck_len, card):
	for line in reversed(instructions.rstrip().split('\n')):
#		print(card, " ", end='')
		if re.match(r'deal into new stack', line) != None:
			card = (deck_len - 1) - card
			print("stack -> ", card)
		elif re.match(r'deal with increment', line) != None:
			inc = int(line.split(' ')[-1])
#			card = (card + deck_len*(abs(inc - card) % inc)) // inc
			new_inc = deck_len - inc
			card = (card * new_inc) % deck_len
#			print("inc ", inc, " -> ", card)
		elif re.match(r'cut', line) != None:
			N = int(line.split(' ')[-1])
			print("cut ", N, " -> ", end='')
			if N < 0: N = deck_len + N
			N = deck_len - N
			if card < N: card += deck_len - N
			else:        card -= N
			print(card)
	return card


dsize = 7
for n in [3,5]:
	t = 'deal with increment %d\n' % (n)
	org = list(range(0, dsize))
	out = [None] * dsize
	orv = [None] * dsize
	fwd = [None] * dsize
	rev = [None] * dsize
	
	for c in org:
		fwd[c] = shuffle_one_card(t, dsize, c)
		rev[c] = invert_shuffle(t, dsize, c)
	for c in org:
		out[fwd[c]] = c
	for c in org:
		orv[rev[c]] = out[c]
	
	print("org %d |  " % n + "  ".join([hex(c)[2:] for c in org]))
	print("orv %d |  " % n + "  ".join([hex(c)[2:] for c in orv]) + (" FAIL" if orv != org else ""))
	print("out %d |  " % n + "  ".join([hex(c)[2:] for c in out]))
	print("rev %d |  " % n + "  ".join([hex(c)[2:] for c in rev]) + (" FAIL" if rev != out else ""))
	print("fwd %d |  " % n + "  ".join([hex(c)[2:] for c in fwd]))
	print()
	
	# print("inc %d | " % n, end='')
	# for c in range(0, dsize):
		# new_loc = shuffle_one_card(t, dsize, c)
		# out[new_loc] = c
	# print(" " + "  ".join([hex(n)[2:] for n in out]))
	
	# print("rev %d | " % n, end='')
	# print(" " + "  ".join([hex(invert_shuffle(t, dsize, c))[2:] for c in range(0,dsize)]))
	# print("rev %d | " % n, end='')
	# out2 = [None] * dsize
	# for c in range(0, dsize):
		# new_loc = invert_shuffle(t, dsize, c)
		# out2[new_loc] = out[c]
	# print(" " + "  ".join([hex(n)[2:] for n in out2]))
	# print()

quit()
t = 'deal with increment 7'
out = shuffle_one_card(t, 10, 2)
print(out)
out = invert_shuffle(t, 10, 4)
print(out)
quit()

out = shuffle_one_card(tin4, 10, 1)
print("1 -> ", out)
out = invert_shuffle(tin4, 10, 4)
print(out)
for n in range(0, 10):
	inst = "deal with increment %d" % 3
	out = invert_shuffle(inst, 10, n)
	print(n, out)

#out = invert_shuffle(instructions, 10007, 8326)
#print("Part 2: ", out)

