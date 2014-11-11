from ALU import *
from myhdl import *
from random import randrange


def test_alu():
	a, b, result = [Signal(intbv(0)[32:]) for i in range(3)]
	sel = Signal(intbv(0)[1:])
	alu_for_test = alu(a, b, sel, result)
	
	@instance
	def monitor():
		print "a      b     sel   result"
		for test in range(5):
			a.next, b.next, sel.next = randrange(10), randrange(10), randrange(2) 
			yield delay(10)
			print "%s   %s   %s   %s" % (hex(a), hex(b), hex(sel), hex(result))

	return monitor

test1 = test_alu()
sim = Simulation(test1)
sim.run(100)