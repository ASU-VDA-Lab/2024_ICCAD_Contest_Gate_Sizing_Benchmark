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

from openroad import Design, Timing
from .check_validity_OpenROAD import check_validity_OpenROAD
import os

def ICCAD_evaluation_OpenROAD(designName: str, design: Design, timing: Timing):
  if check_validity_OpenROAD(designName, design, timing):
    # We only have one corner in this contest
    corner = timing.getCorners()[0]
    # Run Legalization
    site = design.getBlock().getRows()[0].getSite()
    max_disp_x = int(design.micronToDBU(0.1) / site.getWidth())
    max_disp_y = int(design.micronToDBU(0.1) / site.getHeight())
    print("###run legalization###")
    design.getOpendp().detailedPlacement(max_disp_x, max_disp_y, "", False)
    # Run Global Routing and Estimate Global Routing RC
    signal_low_layer = design.getTech().getDB().getTech().findLayer("M1").getRoutingLevel()
    signal_high_layer = design.getTech().getDB().getTech().findLayer("M7").getRoutingLevel()
    clk_low_layer = design.getTech().getDB().getTech().findLayer("M1").getRoutingLevel()
    clk_high_layer = design.getTech().getDB().getTech().findLayer("M7").getRoutingLevel()
    grt = design.getGlobalRouter()
    grt.clear()
    grt.setAllowCongestion(True)
    grt.setMinRoutingLayer(signal_low_layer)
    grt.setMaxRoutingLayer(signal_high_layer)
    grt.setMinLayerForClock(clk_low_layer)
    grt.setMaxLayerForClock(clk_high_layer)
    grt.setAdjustment(0.5)
    grt.setVerbose(False)
    print("###run global routing###")
    grt.globalRoute(False)
    design.evalTclString("estimate_parasitics -global_routing")
    # Start Evaluation
    WNS, maxSlew, maxCap, totalLeakagePower = 0, 0, 0, 0
    # Penalties are subject to change
    WNSPenalty, maxSlewPenalty, maxCapPenalty = 1, 1, 1

    capLimit, slewLimit = 0, 0
    
    # Get all timing metrices
    design.evalTclString("report_wns > evaluation_temp.txt")
    with open ("evaluation_temp.txt", "r") as file:
      for line in file:
        WNS = float(line.split()[1]) / 1000
    for pin_ in design.getBlock().getITerms():
      if pin_.getNet() != None:
        if pin_.getNet().getSigType() != 'POWER' and pin_.getNet().getSigType() != 'GROUND' and pin_.getNet().getSigType() != 'CLOCK':
          library_cell_pin = [MTerm for MTerm in pin_.getInst().getMaster().getMTerms() if (pin_.getInst().getName() + "/" + MTerm.getName()) == pin_.getName()][0]
          if timing.getMaxSlewLimit(library_cell_pin) < timing.getPinSlew(pin_):
            diff = abs(timing.getMaxSlewLimit(library_cell_pin) - timing.getPinSlew(pin_))
            if diff > maxSlewDiff:
              maxSlewDiff = diff
              maxSlew = timing.getPinSlew(pin_, timing.Max) * 1000000000
              slewLimit = timing.getMaxSlewLimit(library_cell_pin) * 1000000000
          if pin_.isOutputSignal():
            if timing.getMaxCapLimit(library_cell_pin) < timing.getNetCap(pin_.getNet(), corner, timing.Max):
              diff = abs(timing.getMaxCapLimit(library_cell_pin) - timing.getNetCap(pin_.getNet(), corner, timing.Max))
              if diff > maxCapDiff:
                maxCapDiff = diff
                maxCap = timing.getNetCap(pin_.getNet(), corner, timing.Max) * 1000000000000
                capLimit = timing.getMaxCapLimit(library_cell_pin) * 1000000000000
    os.remove("evaluation_temp.txt")
    for inst in design.getBlock().getInsts():
      totalLeakagePower += timing.staticPower(inst, corner)
    totalLeakagePower *= 1000000
    # Adjust penalties
    WNSPenalty = 0 if WNS >= 0.0 else WNSPenalty
    maxSlewPenalty = 0 if slew >= maxSlew else maxSlewPenalty
    maxCapPenalty = 0 if capLimit >= maxCap else maxCapPenalty
    
    # Compute score
    score = totalLeakagePower + WNSPenalty * abs(WNS) + maxSlewPenalty * abs(maxSlew) + maxCapPenalty * abs(maxCap)
    print("===================================================")
    print("WNS: %f ns"%(WNS))
    if maxSlewPenalty != 0:
      print("worst Slew: %f ns, Limit: %f ns"%(maxSlew, slewLimit))
    else:
      print("No slew violation")
    if maxCapPenalty != 0:
      print("worst load capacitance: %f pF, Limit: %f pF"%(maxCap, capLimit))
    else:
      print("No load capacitance violation")
    print("total leakage power: %f uW"%(totalLeakagePower))
    print("Score: %f"%score)
    print("===================================================")
    
