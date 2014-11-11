import unittest
import logging
from random import randrange
from myhdl import *
from TimeCount import TimeCount


LOW, HIGH = bool(0), bool(1)
MAX_COUNT = 6*10*10
PERIOD = 10;

#test for count time subsystem
def bench():
	""" Unit test for time counter """
	tens, ones, tenths = [Signal(intbv(0)[4:]) for i in range(3)]
	startstop, reset, clock = [Signal(LOW) for i in range(3)]

	dut = TimeCount(tens, ones, tenths, startstop, reset, clock)

	count = Signal(0)
	counting = Signal(False)

	log = logging.getLogger("LOG")

	@always(delay(PERIOD//2))
	def clkgen():
		clock.next = not clock

	@always(startstop.posedge, reset.posedge)
	def action():
		if reset:
			counting.next = False
			count.next = 0
		else:
			counting.next = not counting

	@always(clock.posedge)
	def counter():
		if counting:
			count.next = (count + 1)% MAX_COUNT

	@always(clock.negedge)
	def monitor():
		a = ((tens*100) + (ones*10) + tenths)
		log.warning(a)# count
		assert ((tens*100) + (ones*10) + tenths) == count

#automatically creates a generator by calling the decorated generator function
	@instance
	def stimulus():
		for maxInterval in (100*PERIOD, 2*MAX_COUNT*PERIOD):
			for sig in (reset, startstop,
                        reset, startstop, startstop,
                        reset, startstop, startstop, startstop,
                        reset, startstop, reset, startstop, startstop, startstop):
				yield delay(rabdrabge(10*PERIOD, maxInterval))
				yield clock.negedge 
				sig.next = HIGH
				yield delay(100)
				sig.next = LOW
		raise StopSimulation

#dut - design under test
#action - defines stopwatch state
#monitor - actual test

	return dut, clkgen, action, counter, monitor, stimulus
	

class  TestTimeCount(unittest.TestCase):
	def test_time_count(self):
		sim = Simulation(bench())
		sim.run	



if __name__ == '__main__':
	unittest.main()
