#// 
#// -------------------------------------------------------------
#//    Copyright 2004-2011 Synopsys, Inc.
#//    Copyright 2010 Mentor Graphics Corporation
#//    Copyright 2010-2011 Cadence Design Systems, Inc.
#//    Copyright 2019-2020 Tuomas Poikela (tpoikela)
#//    All Rights Reserved Worldwide
#// 
#//    Licensed under the Apache License, Version 2.0 (the
#//    "License"); you may not use self file except in
#//    compliance with the License.  You may obtain a copy of
#//    the License at
#// 
#//        http://www.apache.org/licenses/LICENSE-2.0
#// 
#//    Unless required by applicable law or agreed to in
#//    writing, software distributed under the License is
#//    distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#//    CONDITIONS OF ANY KIND, either express or implied.  See
#//    the License for the specific language governing
#//    permissions and limitations under the License.
#// -------------------------------------------------------------
#// 
#
#class tb_env(uvm_component):
    #
    #    `uvm_component_utils(tb_env)
    #
    #    reg_block_slave model; 
    #    apb_agent apb
    #
    #    def __init__(self, name, parent=None)
    #        super().__init__(name,parent)
    #    self.model = None  # type: reg_block_slave
    #    self.apb = None  # type: apb_agent
    #    endfunction
    #
    #   def build_phase(self, phase):
    #        if (model is None):
    #            model = reg_block_slave.type_id.create("model",self)
    #            model.build()
    #            model.lock_model()
    #        end
    #         
    #        apb = apb_agent.type_id.create("apb", self)
    #    endfunction
    #
    #   def connect_phase(self, phase):
    #        if (model.get_parent() is None):
    #            reg2apb_adapter reg2apb = new
    #            model.default_map.set_sequencer(apb.sqr,reg2apb)
    #            model.default_map.set_auto_predict(1)
    #
    #         
    #        end
    #    endfunction
    #    
    #    virtual def void end_of_elaboration(self):
    #        model.print()
    #    endfunction
    #                      
    #endclass
from uvm.base.uvm_component import *
from uvm.macros import *
#
