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
from collections import defaultdict
from pathlib import Path
import os, argparse, sys
sys.path.append("../example/")
sys.path.append("../evaluation/")
from OpenROAD_helper import load_design, get_output_load_pin_cap
from check_validity import check_validity
from evaluation import swap_libcell
import pandas as pd


def updated_dataframe_generate(filePath: str, design: str):
  tech, design = load_design(pyargs.design_name, False)
  timing = Timing(design)
  corner = timing.getCorners()[0]
  if check_validity(filePath, design, timing):
    if swap_libcell(filePath, design):
      # Legalization
      site = design.getBlock().getRows()[0].getSite()
      max_disp_x = int(design.micronToDBU(0.1) / site.getWidth())
      max_disp_y = int(design.micronToDBU(0.1) / site.getHeight())
      design.getOpendp().detailedPlacement(max_disp_x, max_disp_y, "", False)
      # Global routing
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
      grt.globalRoute(False)
      design.evalTclString("estimate_parasitics -global_routing")
      
      block = design.getBlock()
      insts = block.getInsts()
      
      pin_name, maxcap, maxtran, pin_tran, pin_slack = [], [], [], [], []
      pin_rise_arr, pin_fall_arr, input_pin_cap, output_pin_cap = [], [], [], []
      cell_name, cell_static_power = [], []
      for inst in insts:
        pins = inst.getITerms()
        for pin in pins:
          if pin.getNet() != None:
            if pin.getNet().getSigType() != 'POWER' and pin.getNet().getSigType() != 'GROUND':
              library_cell_pin = [MTerm for MTerm in pin.getInst().getMaster().getMTerms() if (pin.getInst().getName() + "/" + MTerm.getName()) == pin.getName()][0]
              pin_name.append(design.getITermName(pin))
              maxcap.append(timing.getMaxCapLimit(library_cell_pin))
              maxtran.append(timing.getMaxSlewLimit(library_cell_pin))              
              pin_tran.append(timing.getPinSlew(pin))
              pin_slack.append(min(timing.getPinSlack(pin, timing.Fall, timing.Max), timing.getPinSlack(pin, timing.Rise, timing.Max)))
              pin_rise_arr.append(timing.getPinArrival(pin, timing.Rise))
              pin_fall_arr.append(timing.getPinArrival(pin, timing.Fall))
              input_pin_cap.append(timing.getPortCap(pin, corner, timing.Max) if pin.isInputSignal() else -1)
              output_pin_cap.append(timing.getNetCap(pin.getNet(), corner, timing.Max) if pin.isOutputSignal() else -1)
        cell_name.append(inst.getName())
        cell_static_power.append(timing.staticPower(inst, corner))
      pin_table = pd.DataFrame({
        "pin_name": pin_name,
        "maxcap": maxcap,
        "maxtran": maxtran,
        "pin_tran": pin_tran,
        "pin_slack": pin_slack,
        "pin_rise_arr": pin_rise_arr,
        "pin_fall_arr": pin_fall_arr,
        "input_pin_cap": input_pin_cap,
        "output_pin_cap": output_pin_cap
        })
      cell_table = pd.DataFrame({
        "cell_name": cell_name,
        "cell_static_power": cell_static_power,
        })
      return cell_table, pin_table
  return None, None

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Output file path and the design name")
  parser.add_argument("--file_path", type = Path, default="./file", action = "store")
  parser.add_argument("--design_name", type = str, default="NaN", action = "store")
  parser.add_argument("--dump_csv", default = False, action = "store_true")
  parser.add_argument("--dump_path", type = str, default="./", action = "store")
  pyargs = parser.parse_args()
  
  cell_df, pin_df = updated_dataframe_generate(pyargs.file_path, pyargs.design_name)
  
  if pyargs.dump_csv:
    if cell_df is not None and pin_df is not None:
      cell_df.to_csv("%scell_properties_update.csv"%pyargs.dump_path, index = False)
      pin_df.to_csv("%spin_properties_update.csv"%pyargs.dump_path, index = False)
