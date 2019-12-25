import copy
import math
import re as regex


class Reaction:
	def __init__(self, output, out_qty, inputs):
		self.output = output
		self.out_qty = out_qty
		self.inputs = inputs
	
	def __repr__(self):
		return "%s => %d %s" % (str(self.inputs), self.out_qty, self.output)

def parse_input_line(line):
	nums = regex.findall(r'\d+', line)
	nums = [int(n) for n in nums]
	names = regex.findall(r'[A-Z]+', line)
	quantities = list(zip(names, nums))
	inputs = quantities[:-1]
	output = quantities[-1]
	return Reaction(output[0], output[1], inputs)

def parse_input(text):
	reactions = {}
	for line in text.splitlines():
		reaction = parse_input_line(line)
		reactions[reaction.output] = reaction
	return reactions
		




class Reactor:
	def __init__(self, reactions):
		self.res = reactions
		self.stock = {}
		self.needed = {}
	
	def __repr__(self):
		return "Needed: " + str(self.needed) + "\nStock: " + str(self.stock) + "\n"
	
	def reverse_consume(self, name, qty):
		if name in self.needed:
			del self.needed[name]
	
		stored = self.stock.get(name, 0)
		if stored >= qty:
			self.stock[name] -= qty
			return
		elif stored > 0:
			qty -= stored
			self.stock[name] = 0
		
		re = self.res[name]
		batches_needed = math.ceil(qty / re.out_qty)
		out_qty = re.out_qty * batches_needed
		self.stock[name] = out_qty - qty
		
		for input in re.inputs:
			in_name = input[0]
			in_qty = input[1]
			if in_name == "ORE":
				self.stock["ORE"] = self.stock.get("ORE", 0) + batches_needed*in_qty
			else:
				self.needed[in_name] = self.needed.get(in_name, 0) + batches_needed*in_qty

	def done(self):
		for ingredient in self.needed:
			if ingredient != "ORE" and self.needed[ingredient] != 0:
				return False
		return True

	def make_from_scratch(self, name, qty):
		self.reverse_consume(name, qty)
		while not self.done():
			next_ingredient = list(self.needed.keys())[0]
			next_qty = self.needed[next_ingredient]
			self.reverse_consume(next_ingredient, next_qty)



test1 = \
"""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

test2 = \
"""9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

test3 = \
"""157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""

with open('input14.txt') as f:
	real_input = f.read()


reactions = parse_input(real_input)
reactor = Reactor(reactions)

reactor.make_from_scratch("FUEL", 1)
ore_min = reactor.stock["ORE"]
print("Part 1: ", ore_min)

needed_ore = 0
goal = 3281000
while True:
	reactor = Reactor(reactions)
	reactor.make_from_scratch("FUEL", goal)
	if reactor.stock["ORE"] > 1000000000000:
		break
	else:
		needed = (goal, reactor.stock["ORE"])
		goal += 1

print("Part 2: ", needed[0], needed[1])
















