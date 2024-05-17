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
      pin_table = pd.DataFrame({
        "pin_name": [],
        "maxcap": [],
        "maxtran": [],
        "pin_tran": [],
        "pin_slack": [],
        "pin_rise_arr": [],
        "pin_fall_arr": [],
        "input_pin_cap": [],
        "output_pin_cap": []
        })
      cell_table = pd.DataFrame({
        "cell_name": [],
        "cell_static_power": [],
        "cell_dynamic_power": []
        })
      
      block = design.getBlock()
      insts = block.getInsts()
      
      for inst in insts:
        pins = inst.getITerms()
        for pin in pins:
          if pin.getNet() != None:
            if pin.getNet().getSigType() != 'POWER' and pin.getNet().getSigType() != 'GROUND':
              pin_entry = pd.DataFrame({
                "pin_name": [design.getITermName(pin)],
                "maxcap": [-1],
                "maxtran": [-1],
                "pin_tran": [timing.getPinSlew(pin)],
                "pin_slack": [min(timing.getPinSlack(pin, timing.Fall, timing.Max), timing.getPinSlack(pin, timing.Rise, timing.Max))],
                "pin_rise_arr": [timing.getPinArrival(pin, timing.Rise)],
                "pin_fall_arr": [timing.getPinArrival(pin, timing.Fall)],
                "input_pin_cap": [timing.getPortCap(pin, corner, timing.Max) if pin.isInputSignal() else "None"],
                "output_pin_cap": [get_output_load_pin_cap(pin, corner, timing) if pin.isOutputSignal() else "None"]
                })
              pin_table = pd.concat([pin_table, pin_entry], ignore_index = True)
        cell_entry = pd.DataFrame({
          "cell_name": [inst.getName()],
          "cell_static_power": [timing.staticPower(inst, corner)],
          "cell_dynamic_power": [timing.dynamicPower(inst, corner)]
          })
        cell_table = pd.concat([cell_table, cell_entry], ignore_index = True)
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
