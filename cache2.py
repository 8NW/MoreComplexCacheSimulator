import argparse, re, random, math

parser = argparse.ArgumentParser(description='A cache simulator')

parser.add_argument('input_file', nargs=1, help='the file that contains the memory trace')
parser.add_argument('cache_ways', nargs=1, help='the number of ways in the cache')
parser.add_argument('cache_sets', nargs=1, help='the number of sets in the cache')

args = parser.parse_args()

cache = {}

cache_ways = int(args.cache_ways[0])
cache_sets = int(args.cache_sets[0])
cache_blocks = cache_sets * cache_ways
input_file = args.input_file[0]

if math.log(cache_ways, 2) != int(math.log(cache_ways, 2)):
	raise ValueError('Cache ways is not a power of two')
if math.log(cache_sets, 2) != int(math.log(cache_sets, 2)):
	raise ValueError('Cache sets is not a power of two')

set_bits = int(math.log(cache_sets, 2))
offset_bits = 2
tag_bits = 32 - set_bits - offset_bits

total_refs = 0
misses = 0

with open(input_file) as f:
	input_data = f.read()
	input_lines = input_data.split('\n')

	for input_line in input_lines:

		input_line = input_line.lstrip()
		input_parts = re.compile(' +').split(input_line)
		#print input_parts
		address_type = input_parts[0]
		input_parts = input_parts[1].split(',')

		address = input_parts[0]
		address_size = input_parts[1]
		
		address_bits = "{:032b}".format(int(address, 16))
		tag = address_bits[:tag_bits]
		line = address_bits[tag_bits:-offset_bits]

		cache_set = cache.get(line, None)


		if cache_set:
			found = 0
			for tags in range(cache_ways):
				current_tag = cache_set[i].get('tag', None)
				if current_tag == None:
					found = 1 
					misses += 1
					cache_set[i]['tag'] = tag
					cache_set[i]['count'] += 1
					break
				elif cache_set[i]['tag'] == tag:
					found = 1
					cache_set[i]['count'] += 1
					break
			if found == 0:
				misses += 1
				randIndex = random.randint(0, cache_ways-1)
				cache_set[randIndex]['tag'] = tag
				cache_set[randIndex]['count'] = 1
		else:
			misses += 1
			cache[line] = [{}]*cache_ways
			cache[line][0]['tag'] = tag
			cache[line][0]['count'] = 1


		# if not cache_line:
		# 	misses += 1
		# 	cache[line] = {}
		# 	cache['tag'] = tag
		# 	cache_line['count'] = 1

		# else: 
		# 	for tags in cache_line:
		# 		if tag == tags 
		# 	if tag == cache[line]['tag']:
		# 		cache[line]['count'] += 1
		# 	else:
		# 		misses += 1
		# 		cache[line]['tag'] = tag
		# 		cache[line]['count'] = 1

		total_refs += 1
			

	print 'Miss rate was: ' + str(misses*100.0/total_refs) + '% out of ' + str(total_refs) + ' references.'




	