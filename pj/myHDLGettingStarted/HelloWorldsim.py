from myhdl import *

def ClkDriver(clk, period = 20):
	lowTime = int(period/2)
	highTime = period - lowTime

	@instance
	def driveClk():
		while True:
			"""similar meaning to "wait" """
			yield delay(lowTime)
			clk.next = 1
			yield delay(highTime)
			clk.next = 0

	return driveClk

def Hello(clk, to="World!"):

	@always(clk.posedge)
	def sayHello():
		print "%s Hello %s" % (now(), to)
	return sayHello

def greetings():
	clk1 = Signal(0)
	clk2 = Signal(0)

	clkdriver_1 = ClkDriver(clk1)
	clkdriver_2 = ClkDriver(clk = clk2, period = 19)
	hello_1 = Hello(clk =clk1)
	hello_2 = Hello(clk = clk2, to = "MyHDL")

	return clkdriver_1, clkdriver_2, hello_1, hello_2

inst = greetings()
sim = Simulation(inst)
sim.run(50)

