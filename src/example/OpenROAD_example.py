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
from openroad import Tech, Design, Timing
import os, odb
from pathlib import Path
from OpenROAD_helper import *

##############################################
# Load the design using OpenROAD Python APIs #
##############################################
print("*****Load design, lib, lef, and sdc*****")
tech, design = load_design("NV_NVDLA_partition_m", False)
timing = Timing(design)
db = ord.get_db()
corner = timing.getCorners()[0]
block = design.getBlock()

#########################################
# Get pins, insts, and nets from OpenDB #
#########################################
print("*****Get pins, insts, and nets from OpenDB*****")
pins = block.getITerms()
insts = block.getInsts()
nets = block.getNets()

# Other ways to get pins from OpenDB
# One way is iterating through insts
for inst in insts:
  inst_ITerms = inst.getITerms()
  for pin in inst_ITerms:
    pass
# The other way is iterating through nets
for net in nets:
  net_ITerms = net.getITerms()
  for pin in net_ITerms:
    pass

#########################
# Get all library cells #
#########################
print("*****Get all library cells*****")
libs = db.getLibs()
for lib in libs:
  for master in lib.getMasters():
    libcell_name = master.getName()
    libcell_area = master.getHeight() * master.getWidth()

#########################################################################
# How to get timing information (pin slew, pin slack, pin arrival time) #
#########################################################################
print("*****get pin's timing information*****")
for pin in pins[12345:12348]:
  # Typically we should use the following if statement to filter out the VDD/VSS pins
  # Since we do not have routed VDD and VSS net in this contest, we can use None instead
  #if pin.getNet().getSigType() != 'POWER' and pin.getNet().getSigType() != 'GROUND':
  if pin.getNet() != None:
    pin_tran = timing.getPinSlew(pin)
    pin_slack = min(timing.getPinSlack(pin, timing.Fall, timing.Max), timing.getPinSlack(pin, timing.Rise, timing.Max))
    pin_rise_arr = timing.getPinArrival(pin, timing.Rise)
    pin_fall_arr = timing.getPinArrival(pin, timing.Fall)
    if pin.isInputSignal():
      input_pin_cap = timing.getPortCap(pin, corner, timing.Max)
    else:
      input_pin_cap = -1
    # This gives the sum of the loading pins' capacitance
    output_load_pin_cap = get_output_load_pin_cap(pin, corner, timing)
    # This will add net's capacitance to the output load capacitance
    output_load_cap = timing.getNetCap(pin.getNet(), corner, timing.Max) if pin.isOutputSignal() else -1
    print("""Pin name: %s
Pin transition time: %.25f
Pin slack: %.25f
Pin rising arrival time: %.25f
Pin falling arrival time: %.25f
Pin's input capacitance: %.25f
Pin's output pin capacitance: %.25f
Pin's output capacitance: %.25f
-------------------------------"""%(
    design.getITermName(pin),
    pin_tran,
    pin_slack,
    pin_rise_arr,
    pin_fall_arr,
    input_pin_cap,
    output_load_pin_cap,
    output_load_cap))
    
#####################################################
# How to get power information (static and dynamic) #
#####################################################
print("*****get instance's power information*****")
for inst in insts[12345:12348]:
  leakage = timing.staticPower(inst, corner)
  internal_and_switching = timing.dynamicPower(inst, corner)
  print("""Instance name: %s
Leakage power: %.25f
Internal power + switching power: %.25f
-------------------------------"""%(
  inst.getName(),
  leakage,
  internal_and_switching))

##############################
# How to perform gate sizing #
##############################
print("*****How to perform gate sizing*****")
timing.makeEquivCells()
# First pick an instance
inst = insts[0]
# Then get the library cell information
inst_master = inst.getMaster()
print("-----------Reference library cell-----------")
print(inst_master.getName())
print("-----Library cells with different sizes-----")
equiv_cells = timing.equivCells(inst_master)
for equiv_cell in equiv_cells:
  print(equiv_cell.getName())
# Perform gate sizing
inst.swapMaster(equiv_cells[0])

########################################################
# Timing information will be updated in the background #
########################################################
print("*****get pin's timing information after gate sizing*****")
for pin in pins[12345:12348]:
  # Typically we should use the following if statement to filter out the VDD/VSS pins
  # Since we do not have routed VDD and VSS net in this contest, we can use None instead
  #if pin.getNet().getSigType() != 'POWER' and pin.getNet().getSigType() != 'GROUND':
  if pin.getNet() != None:
    pin_tran = timing.getPinSlew(pin)
    pin_slack = min(timing.getPinSlack(pin, timing.Fall, timing.Max), timing.getPinSlack(pin, timing.Rise, timing.Max))
    pin_rise_arr = timing.getPinArrival(pin, timing.Rise)
    pin_fall_arr = timing.getPinArrival(pin, timing.Fall)
    if pin.isInputSignal():
      input_pin_cap = timing.getPortCap(pin, corner, timing.Max)
    else:
      input_pin_cap = -1
    # This gives the sum of the loading pins' capacitance
    output_load_pin_cap = get_output_load_pin_cap(pin, corner, timing)
    # This will add net's capacitance to the output load capacitance
    output_load_cap = timing.getNetCap(pin.getNet(), corner, timing.Max) if pin.isOutputSignal() else -1
    print("""Pin name: %s
Pin transition time: %.25f
Pin slack: %.25f
Pin rising arrival time: %.25f
Pin falling arrival time: %.25f
Pin's input capacitance: %.25f
Pin's output pin capacitance: %.25f
Pin's output capacitance: %.25f
-------------------------------"""%(
    design.getITermName(pin),
    pin_tran,
    pin_slack,
    pin_rise_arr,
    pin_fall_arr,
    input_pin_cap,
    output_load_pin_cap,
    output_load_cap))

#######################################################################
# How to use the name of the instance to get the instance from OpenDB #
#######################################################################
inst = block.findInst("FE_OCPC2243_FE_DBTN11_u_NV_NVDLA_cmac_u_core_u_mac_2_mul_136_55_n_2")
print("-------------The instance we get-------------")
print(inst.getName())

###############################################################################
# How to use the name of the library cell to get the library cell from OpenDB #
###############################################################################
master = db.findMaster("INVxp67_ASAP7_75t_R")
print("-----------The library cell we get-----------")
print(master.getName()) 

###########################################
# How to dump the updated design DEF file #
###########################################
odb.write_def(block, "temp.def")
