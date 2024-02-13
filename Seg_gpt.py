from amaranth import *
from amaranth.lib import wiring
from amaranth.build import Platform, ResourceError
from amaranth_boards.nandland_go import NandlandGoPlatform
import itertools

class Main(wiring.Component):
    def __init__(self, platform):
        # super().__init__()
        # Existing initializations
        self.leds = Signal(4)
        self.buttons = Signal(4)

        # 7-segment displays initialization
        seg_1 = platform.request("display_7seg", 0)
        seg_2 = platform.request("display_7seg", 1)
        self.segments_1 = Cat(seg_1.g, seg_1.f, seg_1.e, seg_1.d, seg_1.c, seg_1.b, seg_1.a)
        self.segments_2 = Cat(seg_2.g, seg_2.f, seg_2.e, seg_2.d, seg_2.c, seg_2.b, seg_2.a)

        # New: Clock Divider and Counter Signals
        self.clock_divider_counter = Signal(27)  # Assuming a 50MHz clock, for a 1Hz output
        self.counter_value = Signal(4)  # 4-bit counter for 0-9 values

    def elaborate(self, platform):
        m = Module()
        # Clock Divider Logic
        m.d.sync += self.clock_divider_counter.eq(self.clock_divider_counter + 1)
        with m.If(self.clock_divider_counter == 0):
            m.d.sync += self.counter_value.eq(self.counter_value + 1)
            with m.If(self.counter_value == 9):  # Reset counter after 9
                m.d.sync += self.counter_value.eq(0)

        # Decode Counter Value for 7-Segment Display
        # Simplified example for number 0
        with m.If(self.counter_value == 0):
            m.d.comb += self.segments_1.eq(0b00111111)  # Display "0" on first 7-segment
            # Extend this conditional block for other numbers 1-9

        # Original LED logic
        m.d.comb += self.leds.eq(self.buttons)

        return m

class Top(Elaboratable):
    def elaborate(self, platform):
        m = Module()
        # Existing logic to get resources and instantiate Main
        m.submodules.main = main = Main(platform)

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number))
                except ResourceError:
                    break
            return resources

        for li, led in enumerate([res.o for res in get_all_resources("led")]):
            m.d.comb += led.eq(main.leds[li])
        for bi, button in enumerate([res.i for res in get_all_resources("button")]):
            m.d.comb += main.buttons[bi].eq(button)

        return m

if __name__ == "__main__":
    NandlandGoPlatform().build(Top(), do_program=True, debug_verilog=True)









