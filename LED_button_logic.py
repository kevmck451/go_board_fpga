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

        # LED 1 if button 1 and 2 are pressed 
        m.d.comb += self.leds[0].eq(self.buttons[0] & self.buttons[1])

        # LED 2 if button 1 or 2 are pressed 
        m.d.comb += self.leds[1].eq(self.buttons[0] | self.buttons[1])

        # LED 3 if buttons 3 xor 4 pressed 
        m.d.comb += self.leds[2].eq(self.buttons[2] ^ self.buttons[3])

        # LED 4 if buttons 3 nand 4 pressed
        m.d.comb += self.leds[3].eq(~(self.buttons[2] & self.buttons[3]))


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
