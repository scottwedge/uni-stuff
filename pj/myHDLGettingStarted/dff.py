from myhdl import * 
def dff(q, d, clk):
	@always(clk.posedge)
	def logic():
		q.next = d

	return logic 