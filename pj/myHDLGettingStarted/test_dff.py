#!/usr/bim/env python2
from myhdl import *
from random import randrange
from dff import *

def test_dff():
	q, d, clk = [Signal(bool(0)) for i in range(3)]
	dff_inst = dff(q, d, clk)

	@always(delay(10))
	def clkgen():
		clk.next = not clk

	@always(clk.negedge)
	def stimulus():
		d.next = randrange(2)

	return dff_inst, clkgen, stimulus

def simulate(timesteps):
	sim = Simulation(tb)
	sim.run(timesteps)

simulate(2000)