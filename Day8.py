import sys
import copy
import itertools

def split_layers(image, xsize, ysize):
	layer_size = xsize * ysize
	return [image[p:p+layer_size] for p in range(0, len(image), layer_size)]

with open('Input8.txt') as f:
	image = split_layers([int(i) for i in next(f).strip()], 25, 6)

min_zeros = sys.maxsize
min_result = -1
for layer in image:
	num_zeros = sum([1 if p == 0 else 0 for p in layer])
	num_ones = sum([1 if p == 1 else 0 for p in layer])
	num_twos = sum([1 if p == 2 else 0 for p in layer])
	if num_zeros < min_zeros:
		min_zeros = num_zeros
		min_result = num_ones * num_twos

print("Part 1: %d zeros gives an answer of %d" % (min_zeros, min_result))


def construct_image(image):
	base_output = [2 for p in range(0, len(image[0]))]
	
	for layer in range(0, len(image)):
		for p in range(0, len(image[0])):
			if base_output[p] == 2 and image[layer][p] != 2:
				base_output[p] = image[layer][p]
	
	return base_output

output = construct_image(image)

print("Part 2:")
for y in range(0, 6):
	for x in range(0, 25):
		if output[y*25 + x] == 1:
			print('1', end='')
		else:
			print(' ', end='')
	print("\n", end='')



