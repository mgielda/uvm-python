#//----------------------------------------------------------------------
#//   Copyright 2007-2010 Mentor Graphics Corporation
#//   Copyright 2007-2011 Cadence Design Systems, Inc.
#//   Copyright 2010 Synopsys, Inc.
#//   Copyright 2019 Tuomas Poikela
#//   All Rights Reserved Worldwide
#//
#//   Licensed under the Apache License, Version 2.0 (the
#//   "License"); you may not use this file except in
#//   compliance with the License.  You may obtain a copy of
#//   the License at
#//
#//       http://www.apache.org/licenses/LICENSE-2.0
#//
#//   Unless required by applicable law or agreed to in
#//   writing, software distributed under the License is
#//   distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#//   CONDITIONS OF ANY KIND, either express or implied.  See
#//   the License for the specific language governing
#//   permissions and limitations under the License.
#//----------------------------------------------------------------------

import cocotb
from cocotb.triggers import Timer
#from cocotb.clock import Clock
from uvm.base import run_test, UVMDebug

from test_lib import *
from ubus_if import ubus_if

UBUS_ADDR_WIDTH = 16

#UVMDebug.DEBUG = True

@cocotb.coroutine
def initial_run_test(dut, vif):
    from uvm.base import UVMCoreService
    cs_ = UVMCoreService.get()
    UVMConfigDb.set(None, "*", "vif", vif)
    yield run_test()


@cocotb.coroutine
def initial_reset(vif):
    vif.ubus_reset <= 1
    vif.ubus_clock <= 1
    yield Timer(51, "NS")
    vif.ubus_reset <= 0


@cocotb.coroutine
def always_clk(dut, ncycles):
    dut.ubus_clock <= 0
    n = 0
    print("EEE starting always_clk")
    while n < 2*ncycles:
        n += 1
        yield Timer(5, "NS")
        next_val = not dut.ubus_clock.value
        dut.ubus_clock <= int(next_val)

#module ubus_tb_top;
@cocotb.test()
def module_ubus_tb(dut):

    vif = ubus_if(dut)

    proc_run_test = cocotb.fork(initial_run_test(dut, vif))
    proc_reset = cocotb.fork(initial_reset(dut))
    proc_clk = cocotb.fork(always_clk(dut, 100))
    proc_vif = cocotb.fork(vif.start())

    yield Timer(1000, "NS")
    yield [proc_run_test, proc_clk.join()]
