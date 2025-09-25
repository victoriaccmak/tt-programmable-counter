/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_programmable_counter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    assign uio_oe = 8'h00; // Set all bidirectional pins to input
    wire [7:0] counter_val;
    counter counter_inst (
        .enable(ui_in[0]),
        .clk_in(ui_in[1]),
        .load(ui_in[2]),
        .up_down(ui_in[3]),
        .[7:0] in(uio_in),
        .counter_reg(uo_out),
        .clk(clk),
        .rst_n(rst_n)     // reset_n - low to reset
    );

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in[7:4], uio_out, 1'b0};

endmodule
