def compare_lists(a, b):
	result = a
	for item_b in b:
		if item_b not in a:
			result.append(item_b)
	return result