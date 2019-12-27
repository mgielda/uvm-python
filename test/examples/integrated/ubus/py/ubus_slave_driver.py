#//----------------------------------------------------------------------
#//   Copyright 2007-2010 Mentor Graphics Corporation
#//   Copyright 2007-2011 Cadence Design Systems, Inc.
#//   Copyright 2010 Synopsys, Inc.
#//   Copyright 2019 Tuomas Poikela (tpoikela)
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
from cocotb.triggers import RisingEdge, Timer, FallingEdge

from uvm.base import *
from uvm.comps import UVMDriver
from uvm.macros import uvm_component_utils

from ubus_transfer import *

#//------------------------------------------------------------------------------
#//
#// CLASS: ubus_slave_driver
#//
#//------------------------------------------------------------------------------
#class ubus_slave_driver extends uvm_driver #(ubus_transfer);
class ubus_slave_driver(UVMDriver):

    #  // new - constructor
    def __init__(self, name, parent):
        UVMDriver.__init__(self, name, parent)
        # The virtual interface used to drive and view HDL signals.
        self.vif = None

    def build_phase(self, phase):
        arr = []
        if UVMConfigDb.get(self, "", "vif", arr):
            self.vif = arr[0]
        if self.vif is None:
            self.uvm_report_fatal("NOVIF", "virtual interface must be set for: " +
                self.get_full_name() + ".vif")

    # run phase
    @cocotb.coroutine
    def run_phase(self, phase):
        #    fork
        fork_get = cocotb.fork(self.get_and_drive())
        fork_reset = cocotb.fork(self.reset_signals())
        yield [fork_get, fork_reset.join()]
        #    join
    #  endtask : run_phase


    #  // get_and_drive
    #  virtual protected task get_and_drive();
    @cocotb.coroutine
    def get_and_drive(self):
        yield Timer(0)
        yield FallingEdge(self.vif.sig_reset)
        while True:
            yield RisingEdge(self.vif.sig_clock)
            req = []
            yield self.seq_item_port.get_next_item(req)
            yield self.respond_to_transfer(req[0])
            self.seq_item_port.item_done()
        #  endtask : get_and_drive


    #  // reset_signals
    @cocotb.coroutine
    def reset_signals(self):
        while True:
            yield RisingEdge(self.vif.sig_reset)
            self.vif.sig_error      <= 0
            self.vif.sig_wait       <= 0
            self.vif.slave_en       <= 0
        #  endtask : reset_signals


    #  // respond_to_transfer
    @cocotb.coroutine
    def respond_to_transfer(self, resp):
        if resp.read_write != NOP:
            print("QQQ slave driver responding to " + resp.convert2string())
            self.vif.sig_error <= 0
            for i in range(resp.size):
                if resp.read_write == READ:
                    self.vif.slave_en <= 1
                    self.vif.sig_data_out <= resp.data[i]
                if resp.wait_state[i] > 0:
                    self.vif.sig_wait <= 1
                    for j in range(resp.wait_state[i]):
                        yield RisingEdge(self.vif.sig_clock)
                self.vif.sig_wait <= 0
                yield RisingEdge(self.vif.sig_clock)
                resp.data[i] = int(self.vif.sig_data)
            self.vif.slave_en <= 0
            self.vif.sig_wait  <= 0  # 1'bz
            self.vif.sig_error <= 0  # 1'bz
        else:
            yield Timer(0)
        #  endtask : respond_to_transfer

    #
    #endclass : ubus_slave_driver
#  Provide implementations of virtual methods such as get_type_name and create
uvm_component_utils(ubus_slave_driver)
