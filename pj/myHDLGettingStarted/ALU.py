from myhdl import *

"""alu_func = {"add":      0b0000,
            "sub":      0b0001,
            'mul':      0b0010,
            'inc':      0b0011,
            'dec':      0b0100,
            'not_a':    0b0101,
            'b_and_a':  0b0110,
            'a_or_b':   0b0111}"""

alu_func = enum("add",
                "sub",
                "mul",
                "inc",
                "dec",
                "not_a",
                "b_and_a",
                "a_or_b")

def alu(a, b, operation, result, clk):
    """This module represents an ALU.
    For now it can execute:
    Arithmetic
          add: 0000
          sub: 0001
          inc: 0010
          dec: 0011 ...
    a, b - input 32bits u_sign int
    result - output 32bits
    clk - moment, when alu works"""

    result = Signal(intbv(0)[16:])
    @always(clk.posedge)
    def logic():
        if operation == alu_func.add:
            print "add"
            result.next = a + b
        elif operation == alu_func.sub:
            print "sub"
            result.next = a - b
        elif operation == alu_func.mul:
            print "mul"
            result.next = a * b
        elif operation == alu_func.inc:
            print "inc"
            result.next = a + 1
        elif operation == alu_func.dec:
            print "dec"
            result.next = a - 1
        elif operation ==  alu_func.not_a:
            print "not a"
            result = ~a
        elif operation == alu_func.b_and_a:
            print "a and b"
            result.next = a & b
        elif operation == alu_func.a_or_b:
            print "a or b"
            result.next = a | b
        else:
            print "no such command"
    return logic