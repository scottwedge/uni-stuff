from myhdl import *

def ClkDriver(clk):
	halfPeriod = delay(10)
	period = delay(10)
	@always(halfPeriod)
	def driveClk():
		clk.next = not clk
	return driveClk

def HelloWorld(clk):
	
	@always(clk.posedge)
	def sayHello():
		print "%s Hello positive World!" % now()
	return sayHello

clk = Signal(0)
clkdriver_inst = ClkDriver(clk)
hello_inst = HelloWorld(clk)
sim = Simulation(clkdriver_inst, hello_inst)

sim.run(50)
