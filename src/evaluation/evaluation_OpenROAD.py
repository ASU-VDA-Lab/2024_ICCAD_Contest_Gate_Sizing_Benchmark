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

