from myhdl import *
from random import randrange
from ALU import *

def test_bench():
    #a, b, result = [Signal(intbv(0)[32:]) for i in range(3)]
    a = Signal(intbv(1)[8:])
    b = Signal(intbv(0)[8:])
    result = Signal(0)
    operation = Signal(alu_func["add"])
    clk = Signal(0)
    period = 10

    dut = alu(a, b, operation, result, clk)

    @always(delay(period))
    def clkgen():
        clk.next = not clk

    @instance
    def monitor():
        while True:
            print "a= %s %s b= %s -> result %s" % (a, operation, b, result)
            yield clk.negedge

    def operation(x, y, op):
        a.next = x
        b.next = y
        operation.next = op

            
    """@instance
    def test_add():
        yield operation(1, 2, alu_func["add"])
        yield delay(period//4)
        assert result == 3

    @instance
    def test_sub():
        yield operation(7, 1, alu_func["sub"])
        yield delay(period//4)
        assert result == 6

    @instance
    def test_multiply():
        yield operation(2, 2, alu_func["mul"])
        yield delay(period//4)
        assert result == 4

    @instance
    def test_increment():
        yield operation(2, 5, alu_func["inc"])
        yield delay(period//4)
        assert result == 3

    @instance
    def test_decrement():
        yield operation(9, 2, alu_func["dec"])
        yield delay(period//4)
        assert result == 8

    @instance
    def test_not_a():
        yield operation(5, 1, alu_func["not_a"])
        yield delay(period//4)
        assert result == -6

    @instance
    def test_and():
        yield operation(7, 3, alu_func["b_and_a"])
        yield delay(period//4)
        assert result == 3

    @instance
    def test_or():
        yield operation(5, 9, alu_func["b_or_a"])
        yield delay(period//4)
        assert result == 13"""

    return instances()

test = test_bench()#tb = traceSignals(test_bench)
sim = Simulation(test)        
sim.run(100)