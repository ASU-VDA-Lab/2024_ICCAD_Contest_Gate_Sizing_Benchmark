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
import openroad as ord
from collections import defaultdict

def check_validity_OpenROAD(designName: str, design: Design, timing: Timing):
  # Build original instance name : libcell type map
  correctTypeDict = defaultdict()
  with open("../../design/%s/%s.def"%(designName,designName), "r") as file:
    processLine = False
    skipNext = False
    terminateCounter = 0
    for line in file:
      if terminateCounter == 2:
        break
      if "COMPONENTS" in line:
        processLine = True
        terminateCounter += 1
        continue
      if processLine:
        line = line.split()
        correctTypeDict[line[1]] = line[2]

  # Start examine the correctness of the result
  db = ord.get_db()
  block = design.getBlock()
  timing.makeEquivCells()
  for instName, libcellName in correctTypeDict.items():
    inst = block.findInst(instName)
    if inst == None:
      print("Error: Instance \"%s\" is not in your design."%instName)
    correctMasters = timing.equivCells(db.findMaster(libcellName)) if not (design.isSequential(db.findMaster(libcellName)) or db.findMaster(libcellName).isBlock()) else [db.findMaster(libcellName)]
    masterName = inst.getMaster().getName()
    if masterName not in [correctMaster.getName() for correctMaster in correctMasters]:
      correctMasters = ", ".join([correctMaster.getName() for correctMaster in correctMasters])
      print("Error: Instance \"%s\" should be using the following library cells: %s, but found intending to switch to: %s"%(instName, correctMasters, masterName))
      return False, correctTypeDict
  return True, correctTypeDict

