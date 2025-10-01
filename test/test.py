# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.types import LogicArray


async def half_clk_in(dut, period_ms):
    """Wait for half a clk_in period."""
    start_time = cocotb.utils.get_sim_time(units="ns")
    while True:
        await ClockCycles(dut.clk, 1)
        # Wait for half of the SCLK period (10 us)
        if (start_time + period_ms*1000*1000*0.5) < cocotb.utils.get_sim_time(units="ns"):
            break
    return


def ui_in_logicarray(enable, clk_in, load, up_down):
    """Setup the ui_in value as a LogicArray."""
    return LogicArray(f"0000{up_down}{load}{clk_in}{enable}")


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 100, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.uio_in.value = 0

    # Test counting up
    # Continuously pull clk_in low and high. Make the counter have a period of 0.001ms.
    for i in range(0, 256):
        dut.ui_in.value = ui_in_logicarray(1, 1, 0, 1)
        await half_clk_in(dut, 0.001)
        dut._log.info(f"DEBUG Expected counter {i}, got {(int)(dut.uio_out.value)}")
        assert dut.uio_out.value == i, f"Expected counter {i}, got {(int)(dut.uio_out.value)}"
        dut.ui_in.value = ui_in_logicarray(1, 0, 0, 1)
        await half_clk_in(dut, 0.001)

    # Test load
    # Load in a value of 100
    dut.ui_in.value = ui_in_logicarray(1, 1, 1, 0)
    dut.uio_in.value = 100
    await half_clk_in(dut, 0.001)
    assert dut.uio_out.value == 100, f"Expected counter 100, got {(int)(dut.uio_out.value)}"

    # Test counting down from 100 to 10
    # Continuously pull clk_in low and high. Make the counter have a period of 0.001ms.
    dut.ui_in.value = ui_in_logicarray(1, 0, 0, 0)
    await half_clk_in(dut, 0.001)
    for i in range(99, 9, -1):
        dut.ui_in.value = ui_in_logicarray(1, 1, 0, 0)
        await half_clk_in(dut, 0.001)
        assert dut.uio_out.value == i, f"Expected counter {i}, got {(int)(dut.uio_out.value)}"
        dut.ui_in.value = ui_in_logicarray(1, 0, 0, 0)
        await half_clk_in(dut, 0.001)

    # Test enable
    # Continuously pull clk_in low and high. Make the counter have a period of 0.001ms.
    dut.ui_in.value = ui_in_logicarray(0, 1, 0, 0)
    await half_clk_in(dut, 0.001)
    assert dut.uio_oe.value == 0, f"Expected output enable 0 (for high Z), got {dut.uio_oe.value}"
    dut.ui_in.value = ui_in_logicarray(1, 0, 0, 0)
    await half_clk_in(dut, 0.001)
    assert dut.uio_oe.value == 255, f"Expected output enable 0xFF, got {dut.uio_oe.value}"

    assert True
