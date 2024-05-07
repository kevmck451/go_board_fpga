from amaranth import *
from amaranth.sim import Simulator

class Debouncer(Elaboratable):
    def __init__(self, debounce_time):
        # Initialize debouncer variables
        self.input_signal = Signal()  # Input signal to be debounced
        self.output_signal = Signal()  # Debounced output signal
        self.debounce_time = debounce_time  # Debounce duration in clock cycles

    def elaborate(self, platform):
        m = Module()

        # Counter to track stable duration
        stable_counter = Signal(range(self.debounce_time + 1), reset=0)
        
        # Logic to handle input signal stabilization and update output signal
        with m.If(self.input_signal == self.output_signal):
            # Reset counter if input equals output (stable state)
            m.d.sync += stable_counter.eq(0)
        with m.Else():
            # Increment counter if input != output (potential bounce)
            with m.If(stable_counter < self.debounce_time):
                m.d.sync += stable_counter.eq(stable_counter + 1)
            with m.Else():
                # Update output signal once input is stable for long enough
                m.d.sync += self.output_signal.eq(self.input_signal)
                m.d.sync += stable_counter.eq(0)  # Reset counter after updating output

        return m


def testbench():
    # Simulate a noisy input signal
    yield dut.input_signal.eq(1)
    for _ in range(3):  # Simulate short noise pulses
        yield
    yield dut.input_signal.eq(0)
    for _ in range(10):  # Longer period to observe the debounced output
        print(f"Cycle: {_}, Input: {(yield dut.input_signal)}, Output: {(yield dut.output_signal)}")
        yield

if __name__ == "__main__":
    dut = Debouncer(debounce_time=5)  # Set debounce time as needed
    sim = Simulator(dut)
    sim.add_clock(1e-6)  # Define the simulation clock
    sim.add_sync_process(testbench)
    sim.run()
