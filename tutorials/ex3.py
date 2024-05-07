from amaranth import *
from amaranth.utils import log2_int
from amaranth.sim import Simulator

class TrafficLightController(Elaboratable):
    def __init__(self):
        self.state = Signal(2)  # 2 bits to represent 3 states

    def elaborate(self, platform):
        m = Module()

        # State definitions as integer constants
        GREEN, YELLOW, RED = 0, 1, 2

        # FSM logic
        with m.FSM() as fsm:
            with m.State("GREEN"):
                m.d.sync += self.state.eq(GREEN)
                m.next = "YELLOW"
            with m.State("YELLOW"):
                m.d.sync += self.state.eq(YELLOW)
                m.next = "RED"
            with m.State("RED"):
                m.d.sync += self.state.eq(RED)
                m.next = "GREEN"

        return m


def testbench():
    for _ in range(10):  # Simulate for 10 cycles
        current_state = yield dut.state
        state_str = {0: "GREEN", 1: "YELLOW", 2: "RED"}.get(current_state, "UNKNOWN")
        print(f"Current State: {state_str}")
        yield
        

if __name__ == "__main__":
    dut = TrafficLightController()
    sim = Simulator(dut)
    sim.add_clock(25e-6)  # Simulate a 25 MHz clock frequency
    sim.add_sync_process(testbench)
    sim.run()

