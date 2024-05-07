import itertools

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.build import ResourceError
from amaranth_boards.nandland_go import NandlandGoPlatform

class Main(wiring.Component):
    def __init__(self):
        self.leds = Signal(4)
        self.buttons = Signal(4)

    def elaborate(self, platform):
        m = Module()

        clk_freq = platform.default_clk_frequency
        timer = Signal(range(int(clk_freq//4)), reset=int(clk_freq//4) - 1)
        flops = Signal(len(self.leds))

        # m.d.comb += self.leds.eq(flops ^ self.buttons)
        m.d.comb += self.leds.eq(flops)
        with m.If(timer == 0):
            m.d.sync += timer.eq(timer.reset)
            m.d.sync += flops.eq(~flops)
        with m.Else():
            m.d.sync += timer.eq(timer - 1)

        return m

class Top(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        def get_all_resources(name):
            resources = []
            for number in itertools.count():
                try:
                    resources.append(platform.request(name, number))
                except ResourceError:
                    break
            return resources

        m.submodules.main = main = Main()

        for li, led in enumerate([res.o for res in get_all_resources("led")]):
            m.d.comb += led.eq(main.leds[li])
        for bi, button in enumerate([res.i for res in get_all_resources("button")]):
            m.d.comb += main.buttons[bi].eq(button)

        return m

if __name__ == "__main__":
    NandlandGoPlatform().build(Top(), do_program=True, debug_verilog=True)
