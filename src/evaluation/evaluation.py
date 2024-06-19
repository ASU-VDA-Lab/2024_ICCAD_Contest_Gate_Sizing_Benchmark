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

from openroad import Tech, Design, Timing
import openroad as ord
import odb
from check_validity import check_validity
from collections import defaultdict
from pathlib import Path
import os, argparse, sys

def swap_libcell(filePath: str, design: Design):
  # Build original instance name : libcell type map
  changeTypeDict = defaultdict()
  with open(filePath, "r") as file:
    for line in file:
      line = line.split()
      changeTypeDict[line[0]] = line[1]

  # Start examine the correctness of the result
  db = ord.get_db()
  for inst in design.getBlock().getInsts():
    if inst.getName() not in changeTypeDict:
      print("Error: Instance \"%s\" is not ins the output .size file"%inst.getName())
      return False
    inst.swapMaster(db.findMaster(changeTypeDict[inst.getName()]))
  return True
  
def ICCAD_evaluation(filePath: str, design: Design, timing: Timing, equivcell_dict: dict):
  if check_validity(filePath, design, timing, equivcell_dict):
    if swap_libcell(filePath, design):
      # We only have one corner in this contest
      corner = timing.getCorners()[0]
      # Legalization
      site = design.getBlock().getRows()[0].getSite()
      max_disp_x = int(design.micronToDBU(0.1) / site.getWidth())
      max_disp_y = int(design.micronToDBU(0.1) / site.getHeight())
      print("Legalizing...")
      design.getOpendp().detailedPlacement(max_disp_x, max_disp_y, "", False)
      # Global Route and Estimate Global Route RC
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
      print("Run Global Routing...")
      grt.globalRoute(False)
      design.evalTclString("estimate_parasitics -global_routing")
      # Start Evaluation
      WNS, maxSlew, maxCap, totalLeakagePower = 0, 0, 0, 0
      # Penalties are subject to change
      WNSPenalty, maxSlewPenalty, maxCapPenalty = 1, 1, 1

      capLimit, slewLimit = 0, 0
      maxCapDiff, maxSlewDiff = 0, 0
      # Get all timing metrices
      design.evalTclString("report_wns > wns_evaluation_temp.txt")
      with open ("wns_evaluation_temp.txt", "r") as file:
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

      os.remove("wns_evaluation_temp.txt")
      for inst in design.getBlock().getInsts():
        totalLeakagePower += timing.staticPower(inst, corner)
      totalLeakagePower *= 1000000
      # Adjust penalties
      WNSPenalty = 0 if WNS >= 0.0 else WNSPenalty
      maxSlewPenalty = 0 if slewLimit >= maxSlew else maxSlewPenalty
      maxCapPenalty = 0 if capLimit >= maxCap else maxCapPenalty
      
      # Compute score
      score = totalLeakagePower + WNSPenalty * abs(WNS) + maxSlewPenalty * abs(maxSlew) + maxCapPenalty * abs(maxCap)
      print("===================================================")
      print("WNS: %f ns"%(WNS))
      if maxSlewPenalty != 0:
        print("Worst slew: %f ns, Limit: %f ns"%(maxSlew, slewLimit))
      else:
        print("No slew violation")
      if maxCapPenalty != 0:
        print("Worst load capacitance: %f pF, Limit: %f pF"%(maxCap, capLimit))
      else:    
        print("No load capacitance violation")
      print("Total leakage power: %f uW"%(totalLeakagePower)) 
      print("Score: %f"%score)
      print("===================================================")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Output file path and the design name")
  parser.add_argument("--file_path", type = Path, default="./file", action = "store")
  parser.add_argument("--design_name", type = str, default="NaN", action = "store")
  parser.add_argument("--dump_def", default = False, action = "store_true")
  parser.add_argument("--equivcell_file_path", type = str, default = "../../platform/ASAP7/libcell_id.csv")
  pyargs = parser.parse_args()
  
  sys.path.append("../example/")
  from OpenROAD_helper import load_design, build_libcell_dict

  tech, design = load_design(pyargs.design_name, False)
  timing = Timing(design)
  equivcell_dict = build_libcell_dict(pyargs.equivcell_file_path)
  ICCAD_evaluation(pyargs.file_path, design, timing, equivcell_dict)
  
  if pyargs.dump_def:
    odb.write_def(design.getBlock(), "%s.def"%pyargs.design_name)
