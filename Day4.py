def check_password(pw):
	d = [(pw // (10 ** n)) % 10 for n in range(5, -1, -1)]
	if d[0] == d[1] or d[1] == d[2] or d[2] == d[3] or d[3] == d[4] or d[4] == d[5]:
		if d[0] <= d[1] and d[1] <= d[2] and d[2] <= d[3] and d[3] <= d[4] and d[4] <= d[5]:
			return True
	return False

tests = [111111, 223450, 123789]

print([check_password(p) for p in tests])

count = 0
for p in range(265275, 781584+1):
	if check_password(p):
		count += 1

print("Part 1 answer: ", count)

def check_password2(pw):
	d = [(pw // (10 ** n)) % 10 for n in range(5, -1, -1)]

	if d[0] <= d[1] and d[1] <= d[2] and d[2] <= d[3] and d[3] <= d[4] and d[4] <= d[5]:
		if (d[0] == d[1] and d[1] != d[2]) or \
		  (d[1] == d[2] and d[0] != d[1] and d[2] != d[3]) or \
		  (d[2] == d[3] and d[1] != d[2] and d[3] != d[4]) or \
		  (d[3] == d[4] and d[2] != d[3] and d[4] != d[5]) or \
		  (d[4] == d[5] and d[3] != d[4]):
			return True
	return False

tests2 = [112233, 123444, 111122]
print([check_password2(p) for p in tests2])

count = 0
for p in range(265275, 781584+1):
	if check_password2(p):
		count += 1

print("Part 2 answer: ", count)