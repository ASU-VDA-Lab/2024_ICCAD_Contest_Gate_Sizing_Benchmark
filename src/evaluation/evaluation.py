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
  
def ICCAD_evaluation(filePath: str, design: Design, timing: Timing):
  if check_validity(filePath, design, timing):
    if swap_libcell(filePath, design):
      WNS, maxSlew, maxCap, totalLeakagePower = 0, 0, 0, 0
      WNSPenalty, maxSlewPenalty, maxCapPenalty = 1, 1, 1

      capLimit = 0
      
      # Get all timing metrices
      design.evalTclString("report_wns > evaluation_temp.txt")
      with open ("evaluation_temp.txt", "r") as file:
        for line in file:
          WNS = float(line.split()[1])
      design.evalTclString("report_check_types -max_cap > evaluation_temp.txt")
      with open ("evaluation_temp.txt", "r") as file:
        for line in file:
          if len(line.split()) != 0:
            maxCap = line
        maxCap = float(maxCap.split()[2])
      design.evalTclString("report_check_types -max_slew > evaluation_temp.txt")
      with open ("evaluation_temp.txt", "r") as file:
        for line in file:
          if len(line.split()) != 0:
            maxSlew = line
            capLimit = line
        maxSlew = float(maxSlew.split()[2])
        capLimit = float(capLimit.split()[1])
      os.remove("evaluation_temp.txt")
      # We only have one corner in this contest
      corner = timing.getCorners()[0]
      for inst in design.getBlock().getInsts():
        totalLeakagePower += timing.staticPower(inst, corner)
      
      # Adjust penalties
      WNSPenalty = 0 if WNS >= 0.0 else WNSPenalty
      maxSlewPenalty = 0 if 320 >= maxSlew else maxSlewPenalty
      maxCapPenalty = 0 if capLimit >= maxCap else maxCapPenalty
      
      # Compute score
      score = totalLeakagePower + WNSPenalty * abs(WNS) + maxSlewPenalty * abs(maxSlew) + maxCapPenalty * abs(maxCap)
      print("===================================================")
      print("WNS: %f ps, worst Slew: %f ps"%(WNS, maxSlew))
      print("worst load capacitance: %f fF, total leakage power: %f W"%(maxCap, totalLeakagePower)) 
      print("Score: %f"%score)
      print("===================================================")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Output file path and the design name")
  parser.add_argument("--file_path", type = Path, default="./file", action = "store")
  parser.add_argument("--design_name", type = str, default="NaN", action = "store")
  parser.add_argument("--dump_def", default = False, action = "store_true")
  pyargs = parser.parse_args()
  
  sys.path.append("../example/")
  from OpenROAD_helper import load_design

  tech, design = load_design(pyargs.design_name, False)
  timing = Timing(design)
  
  ICCAD_evaluation(pyargs.file_path, design, timing)
  
  if pyargs.dump_def:
    odb.write_def(design.getBlock(), "%s.def"%pyargs.design_name)
