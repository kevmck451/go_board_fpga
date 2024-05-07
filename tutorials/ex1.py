from amaranth import *
from amaranth.sim import Simulator, Settle

class ANDGate(Elaboratable):
    def elaborate(self, platform):
        m = Module()
        self.input1 = Signal()
        self.input2 = Signal()
        self.output = Signal()
        m.d.comb += self.output.eq(self.input1 & self.input2)
        return m

def testbench():
    yield dut.input1.eq(1)
    yield dut.input2.eq(0)
    yield Settle()  # Allow signals to propagate
    print(f"Input: 1 & 0, Output: {(yield dut.output)}")
    assert (yield dut.output) == 0
    yield dut.input1.eq(1)
    yield dut.input2.eq(1)
    yield Settle()  # Allow signals to propagate
    print(f"Input: 1 & 1, Output: {(yield dut.output)}")
    assert (yield dut.output) == 1


if __name__ == "__main__":
    dut = ANDGate()
    sim = Simulator(dut)
    sim.add_process(testbench)
    sim.run()
    print('Everything ran correctly bitch')
