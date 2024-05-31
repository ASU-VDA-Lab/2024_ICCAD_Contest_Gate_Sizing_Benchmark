#BSD 3-Clause License
#
#Copyright (c) 2024, ASU-VDA-Lab
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import openroad as ord
from openroad import Tech, Design
import os, odb
from pathlib import Path

def load_design(design_name, verilog = False):
  tech = Tech()
  libDir = Path("../../platform/ASAP7/lib/")
  lefDir = Path("../../platform/ASAP7/lef/")
  designDir = Path("../../design/%s"%design_name)

  # Read technology files
  libFiles = libDir.glob('*.lib')
  lefFiles = lefDir.glob('*.lef')
  for libFile in libFiles:
    tech.readLiberty(libFile.as_posix())
  tech.readLef("%s/%s"%(lefDir.as_posix(), "asap7_tech_1x_201209.lef"))
  for lefFile in lefFiles:
    tech.readLef(lefFile.as_posix())
  design = Design(tech)

  # Read design files
  if verilog:
    verilogFile = "%s/%s.v"%(designDir.as_posix(), design_name)
    design.readVerilog(verilogFile)
    design.link(design_name)
  else:
    defFile = "%s/%s.def"%(designDir.as_posix(), design_name)
    design.readDef(defFile)

  # Read the SDC file, SPEF file, and set the clocks
  spefFile = "%s/%s.spef"%(designDir.as_posix(), design_name)
  design.evalTclString("read_spef %s"%spefFile)
  sdcFile = "%s/%s.sdc"%(designDir.as_posix(), design_name)
  design.evalTclString("read_sdc %s"%sdcFile)
  design.evalTclString("source ../../platform/ASAP7/setRC.tcl")
  
  # Global connect
  VDDNet = design.getBlock().findNet("VDD")
  if VDDNet is None:
    VDDNet = odb.dbNet_create(design.getBlock(), "VDD")
  VDDNet.setSpecial()
  VDDNet.setSigType("POWER")
  VSSNet = design.getBlock().findNet("VSS")
  if VSSNet is None:
    VSSNet = odb.dbNet_create(design.getBlock(), "VSS")
  VSSNet.setSpecial()
  VSSNet.setSigType("GROUND")
  design.getBlock().addGlobalConnect(None, ".*", "VDD", VDDNet, True)
  design.getBlock().addGlobalConnect(None, ".*", "VSS", VSSNet, True)
  design.getBlock().globalConnect()

  return tech, design

#################################################
# Get the load pin capacitance of an output pin #
#################################################
def get_output_load_pin_cap(pin, corner, timing):
  # first check if the pin is an output pin
  if pin.isOutputSignal():
    output_load_pin_cap = 0
    # loop through all pins connected to this pin (including this pin)
    for net_pin in pin.getNet().getITerms():
      # get the downstream input pin caps
      if net_pin.isInputSignal():
        output_load_pin_cap += timing.getPortCap(net_pin, corner, timing.Max)
    return output_load_pin_cap
  else:
    return -1


