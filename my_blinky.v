module blinky (input clk, input rst, output [3:0] leds, input [3:0] buttons);
assign leds[0] = buttons[0] & buttons[1];
endmodule
