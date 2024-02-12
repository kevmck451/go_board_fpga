import itertools

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.build import ResourceError
from amaranth_boards.nandland_go import NandlandGoPlatform

class Main(wiring.Component):
    leds: Out(4)
    buttons: In(4)

    def elaborate(self, platform):
        m = Module()

        # All LEDs on
        # m.d.comb += self.leds.eq(0b1111)

        # Button 1 turns on all LEDs
        # m.d.comb += self.leds.eq(Cat(self.buttons[0], self.buttons[0], self.buttons[0], self.buttons[0]))
        
        # Each button turns on related LED
        m.d.comb += self.leds.eq(Cat(self.buttons[0], self.buttons[1], self.buttons[2], self.buttons[3]))

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

        m.submodules.blinky = main = Main()

        for li, led in enumerate([res.o for res in get_all_resources("led")]):
            m.d.comb += led.eq(main.leds[li])
        for bi, button in enumerate([res.i for res in get_all_resources("button")]):
            m.d.comb += main.buttons[bi].eq(button)

        return m

if __name__ == "__main__":
    NandlandGoPlatform().build(Top(), do_program=True, debug_verilog=True)
