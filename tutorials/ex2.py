from amaranth import *
from amaranth.sim import Simulator

class Counter(Elaboratable):
    def __init__(self, max_value):
        self.max_value = max_value
        # The counter's current value
        self.value = Signal(range(max_value))

    def elaborate(self, platform):
        m = Module()

        # Increment the counter on each clock cycle
        with m.If(self.value == self.max_value - 1):
            m.d.sync += self.value.eq(0)
        with m.Else():
            m.d.sync += self.value.eq(self.value + 1)

        return m



def testbench():
    # Let's run the simulation for a few cycles to observe the counter.
    for _ in range(10):
        print(f"Counter Value: {(yield dut.value)}")
        yield

if __name__ == "__main__":
    max_value = 5
    dut = Counter(max_value=max_value)
    sim = Simulator(dut)
    sim.add_clock(25e-6)  # Simulate a 25 MHz clock
    sim.add_sync_process(testbench)
    sim.run()
