from myhdl import *
from random import randrange
from unittest import TestCase

def bin2gray(B, G, width):
    """Gray encoder
    B - input intbv signal, binary encoded
    G - output intbv signal, gray encoded"""

    @always_comb
    def logic():
        for i in range(width):
            G.next[i] = B[i+1]^B[i]
    return logic

class TestGrayCodeProperties(TestCase):

    def testSingleBitChange(self):
        """checking out proper change of a singke bit"""
        def test(B, G, width):
            B.next = intbv(0)
            yield delay(10)
            for i in range(1, 2**width):
                G_Z.next = G
                B.next = intbv(i)
                yield delay(10)
                diffcode = bin(G^G_Z)
                print diffcode.count('1') +" and " + '1'
                self.assertEqual(diffcode.count('1'), 1)

        for width in range(1, MAX_WIDTH):
            B = Signal(intbv(-1))
            G = Signal(intbv(0))
            G_Z = Signal(intbv(0))
            dut = bin2gray(B, G, width)
            check = test(B, G, width)
            sim = Simulation(dut, check)
            sim.run(quiet = 1)

    def testUniqueCodeWords(self):
        """Check that all codewords occur exactly once"""
        def test(B, G, width):
            for i in range(2**width):
                B.next = intbv(i)
                yield delay(10)
                actual.append(int(G))
            actual.sort()
            expected = range(2**width)
            print acual + ' and ' + expected
            self.assertEqual(actual, expected)

        for width in range(1, MAX_WIDTH):
            B = Signal(intbv(-1))
            G = Signal(intbv(0))
            dut = bin2gray(B, G, width)
            check = test(B, G, width)
            sim = Simulation(dut, check)
            sim.run(quiet=1)




    
