
Skip to content
Using Gmail with screen readers
Advent of Code day 6
Inbox
	x
Adam Haun <adamhaun@gmail.com>
	
AttachmentsMon, Dec 9, 9:53 AM (5 days ago)
	
to Me

-- 
Adam Haun
adamhaun@gmail.com
Attachments area
	
	
	

# Advent of Code

import copy


class Body:
	def __init__(self, dict, name, central_body):
		self.dict = dict
		self.name = name
		self.central_body = central_body
	
	def __repr__(self):
		return self.name + "->" + self.central_body
	
	def parent(self):
		return self.dict[self.central_body]

def build_orbit_graph(orbits):
	graph = {"COM":Body({}, "COM", "")}
	for o in orbits:
		bodies = o.strip().split(')')
		if bodies == [""]: continue
		graph[bodies[1]] = Body(graph, bodies[1], bodies[0])
	return graph

def get_parent_chain(body):
	if body.name == "COM":
		return []
	else:
		p = body.parent()
		return [p.name] + get_parent_chain(p)

def count_orbits(body):
	if body.name == "COM":
		return 0
	else:
		return 1 + count_orbits(body.parent())



test_orbits = """
	COM)B
	B)C
	C)D
	D)E
	E)F
	B)G
	G)H
	D)I
	E)J
	J)K
	K)L
	K)YOU
	I)SAN
"""

test_graph = build_orbit_graph(test_orbits.split('\n'))
print(count_orbits(test_graph['D']))
print(count_orbits(test_graph['L']))
print(count_orbits(test_graph['COM']))
test_you_chain = get_parent_chain(test_graph['YOU'])
test_san_chain = get_parent_chain(test_graph['SAN'])
test_common_chain = [b for b in test_you_chain if b in test_san_chain]
test_nearest_common = test_graph[test_common_chain[0]]
num_transfers = count_orbits(test_graph['YOU'].parent()) + count_orbits(test_graph['SAN'].parent()) - 2*count_orbits(test_nearest_common)
print(num_transfers)

with open('input6.txt') as f:
	orbit_graph = build_orbit_graph(f)
orbit_counts = [count_orbits(orbit_graph[o]) for o in orbit_graph]

print("Part 1 answer: ", sum(orbit_counts))


you_chain = get_parent_chain(orbit_graph['YOU'])
san_chain = get_parent_chain(orbit_graph['SAN'])
common_chain = [b for b in you_chain if b in san_chain]
nearest_common = orbit_graph[common_chain[0]]
num_transfers = count_orbits(orbit_graph['YOU'].parent()) + count_orbits(orbit_graph['SAN'].parent()) - 2*count_orbits(nearest_common)
print("Part 2 answer: ", num_transfers)
