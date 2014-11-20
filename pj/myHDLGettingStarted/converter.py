def digitConverter(int a):
	result = []
	if a > 2**32 -1 && a < -(2**32):
		print "The number is too large"
		return 1
	else:
		for i in range(a//2+1):
			b = a % 2
			a = int(a/2)
			result.append(b)
			result.reverse()
		return str(result)
