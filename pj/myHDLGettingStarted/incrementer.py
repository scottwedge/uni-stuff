from myhdl import *
from random import *

ACTIVE__LOW, INACTIE_HIGH = 0, 1

def Inc(count, enable, clock, reset, n):
	
	@always_seq(clock.posedge, reset = reset)
	def incLogic():
		if enable:
			count.next = (count + 1) % n 

	return incLogic

#for testbench indipendant clock generator will be used
def testbench():
	count, enable, clock = [Signal(intbv(0)) for i in range(3)]
	reset = ResetSignal(0, active = ACTIVE__LOW, async = True)

	inc_1 = Inc(count, enable, clock, reset, n = 4)
	HALF_PERIOD = delay(10)

	@always(HALF_PERIOD)
	def clockGen():
		clock.next = not clock

	@instance
	def stimulus():
		reset.next = ACTIVE__LOW
		yield clock.negedge
		reset.next = INACTIE_HIGH
		for i in range(12):
			enable.next = min(1, randrange(3))
			yield clock.negedge
		raise StopSimulation

	@instance
	def monitor():
		print "enable count"
		yield reset.posedge
		while 1:
			yield clock.posedge
			yield delay(1)
			print " %s    %s" % (enable, count)

	return clockGen, stimulus,  inc_1, monitor,

tb = testbench()
sim = Simulation(tb)
tb = traceSignals(testbench)
sim.run()