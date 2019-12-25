import colorama
colorama.init()

# Part 1: Simple fuel calculation for each module mass
def calc_fuel(mass):
	return (mass // 3) - 2

print("Mass 12: ", calc_fuel(12))
print("Mass 14: ", calc_fuel(14))
print("Mass 1969: ", calc_fuel(1969))
print("Mass 100756: ", calc_fuel(100756))

with open('input1.txt', 'r') as f:
	masses = [int(n) for n in f]
print("\x1b[32;1mPart 1 fuel required: ", sum([calc_fuel(m) for m in masses]), "\x1b[0m")


# Part 2: Recursive calculation for added fuel
def calc_recursive_fuel(mass):
	f = calc_fuel(mass)
	if f <= 0:
		return 0
	else:
		return f + calc_recursive_fuel(f)

print("Mass 14: ", calc_recursive_fuel(14))
print("Mass 1969: ", calc_recursive_fuel(1969))
print("Mass 100756: ", calc_recursive_fuel(100756))

fuel_req = sum(map(calc_recursive_fuel, masses))
print("\x1b[32;1mPart 2 fuel required: ", fuel_req, "\x1b[0m")