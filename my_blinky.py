import itertools

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.build import ResourceError
from amaranth_boards.nandland_go import NandlandGoPlatform

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

        leds = Signal(4)
        buttons = Signal(4)

        m.submodules.blinky = blinky = Instance("blinky",
            o_leds=leds, i_buttons=buttons, i_clk=ClockSignal(), i_rst=ResetSignal())

        for li, led in enumerate([res.o for res in get_all_resources("led")]):
            m.d.comb += led.eq(leds[li])
        for bi, button in enumerate([res.i for res in get_all_resources("button")]):
            m.d.comb += buttons[bi].eq(button)

        return m

if __name__ == "__main__":
    p = NandlandGoPlatform()
    p.add_file("my_blinky.v", open("my_blinky.v").read())
    p.build(Top(), do_program=True, debug_verilog=True)
