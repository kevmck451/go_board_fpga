import itertools

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.build import ResourceError
from amaranth_boards.nandland_go import NandlandGoPlatform

import seven_seg_logic


class Main(wiring.Component):
    def __init__(self, platform):
        self.leds = Signal(4)
        self.buttons = Signal(4)

        seg_1 = platform.request("display_7seg", 0)
        seg_2 = platform.request("display_7seg", 1)

        self.segments_1 = Cat(seg_1.g, seg_1.f, seg_1.e, seg_1.d, seg_1.c, seg_1.b, seg_1.a)
        self.segments_2 = Cat(seg_2.g, seg_2.f, seg_2.e, seg_2.d, seg_2.c, seg_2.b, seg_2.a)

    def elaborate(self, platform):
        m = Module()

        # 7 Seg Display All Lit
        # m.d.comb += self.segments_1.eq(0b1111111)  
        # m.d.comb += self.segments_2.eq(0b1111111) 

        counter = 0
        # Each button turns on related LED
        # m.d.comb += self.leds.eq(self.buttons)
        with m.If(self.buttons[2] == 1):
            m.d.comb += 



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

        m.submodules.main = main = Main(platform)

        for li, led in enumerate([res.o for res in get_all_resources("led")]):
            m.d.comb += led.eq(main.leds[li])
        for bi, button in enumerate([res.i for res in get_all_resources("button")]):
            m.d.comb += main.buttons[bi].eq(button)

        return m

if __name__ == "__main__":
    NandlandGoPlatform().build(Top(), do_program=True, debug_verilog=True)
