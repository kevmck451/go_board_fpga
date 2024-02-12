import itertools

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.build import ResourceError
from amaranth_boards.nandland_go import NandlandGoPlatform

class Main(wiring.Component):
    def __init__(self):

        # This works, but can only be treated as group and cant be accessed individually
        # self.leds = Out(4)
        # self.buttons = In(4)

        # This works for both group and individual:
        self.leds = Signal(4)
        self.buttons = Signal(4)

        # You can also define things individually if needed:
        # self.led0 = Signal(1)
        # self.led1 = Signal(1)
        # self.led2 = Signal(1)
        # self.led3 = Signal(1)
        # self.button0 = Signal(1)
        # self.button1 = Signal(1)
        # self.button2 = Signal(1)
        # self.button3 = Signal(1)

    def elaborate(self, platform):
        m = Module()

        # Example 1
        # -----------------------------------------
        # All LEDs on
        # m.d.comb += self.leds.eq(0b1111)

        # Could also be done like this:
        # m.d.comb += self.leds[0].eq(0b1)
        # m.d.comb += self.leds[1].eq(0b1)
        # m.d.comb += self.leds[2].eq(0b1)
        # m.d.comb += self.leds[3].eq(0b1)

        # Example 2
        # -----------------------------------------
        # Button 1 turns on all LEDs
        # m.d.comb += self.leds.eq(Cat(self.buttons[0], self.buttons[0], self.buttons[0], self.buttons[0]))

        # Could also be done like this:
        # m.d.comb += self.leds[0].eq(self.buttons[0])
        # m.d.comb += self.leds[1].eq(self.buttons[0])
        # m.d.comb += self.leds[2].eq(self.buttons[0])
        # m.d.comb += self.leds[3].eq(self.buttons[0])


        # Example 3
        # -----------------------------------------
        # Each button turns on related LED
        # m.d.comb += self.leds.eq(Cat(self.buttons[0], self.buttons[1], self.buttons[2], self.buttons[3]))

        # Could also be done like this:
        m.d.comb += self.leds.eq(self.buttons)


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
