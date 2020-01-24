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
		print(card, " ", end='')
		if re.match(r'deal into new stack', line) != None:
			card = (deck_len - 1) - card
			print("stack -> ", card)
		elif re.match(r'deal with increment', line) != None:
			inc = int(line.split(' ')[-1])
			card = (card + deck_len*(abs(inc - card) % inc)) // inc
			print("inc ", inc, " -> ", card)
		elif re.match(r'cut', line) != None:
			N = int(line.split(' ')[-1])
			print("cut ", N, " -> ", end='')
			if N < 0: N = deck_len + N
			N = deck_len - N
			if card < N: card += deck_len - N
			else:        card -= N
			print(card)
	return card

out = shuffle_one_card(tin4, 10, 1)
#print(out)
#out = invert_shuffle(tin4, 10, 4)
#print(out)
for n in range(0, 10):
	inst = "deal with increment %d" % 3
	out = invert_shuffle(inst, 10, n)
	print(n, out)

#out = invert_shuffle(instructions, 10007, 8326)
#print("Part 2: ", out)

