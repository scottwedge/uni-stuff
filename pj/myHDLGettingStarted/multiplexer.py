from myhdl import *
from random import randrange

def Mux(z, a, b, sel):

	@always_comb
	def muxLogic():
		if sel==1:
			z.next = a
		else:
			z.next = b
	return muxLogic

z, a, b, sel = [Signal(0) for i in range(4)]
mux_1 = Mux(z, a, b, sel)

def test():
	print "z a b sel"
	for i in range(8):
		a.next, b.next, sel.next = randrange(8), randrange(8), randrange(2) 
		yield delay(10)
		print "%s %s %s %s" % (z, a, b, sel)

test_1 = test()

sim = Simulation(mux_1, test_1)
sim.run()