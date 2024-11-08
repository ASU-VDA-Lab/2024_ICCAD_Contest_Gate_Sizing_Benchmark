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
import graph_tool as gt
import pickle
import numpy as np
import pandas as pd
import sys
import argparse
from pathlib import Path

#############################################################################################
#LPG dataframe properties:                                                                  #
#('id' maps to the node id in LPG)                                                          #
#pin_df: 'name', 'x', 'y', 'is_in_clk', 'is_port', 'is_start', 'is_end', 'dir',             #
#        'maxcap', 'maxtran', 'num_reachable_endpoint', 'cellname', 'netname',              #
#        'tran', 'slack', 'risearr', 'fallarr', 'cap', 'is_macro', 'is_seq',                #
#        'is_buf', 'is_inv', 'new_cellname', 'new_netname', 'id'                            #
#                                                                                           #
#cell_df: 'name', 'is_seq', 'is_macro', 'is_in_clk', 'x0', 'y0', 'x1', 'y1',                #
#         'is_buf', 'is_inv', 'ref', 'staticpower', 'dynamicpower', 'x', 'y',               #
#         'new_cellname', 'id'                                                              #
#                                                                                           #
#net_df: 'name', 'net_route_length', 'net_steiner_length', 'fanout', 'total_cap',           #
#        'net_cap', 'net_coupling', 'net_res', 'id'                                         #
#                                                                                           #
#fo4_df: 'ref', 'func_id', 'libcell_area', 'worst_input_cap', 'libcell_leakage',            #
#        'fo4_delay', 'libcell_delay_fixed_load', 'libcell_id'                              #
#                                                                                           #
#pin_pin_df: 'src', 'tar', 'src_type', 'tar_type', 'is_net', 'arc_delay', 'src_id', 'tar_id'#
#cell_pin_df: 'src', 'tar', 'src_type', 'tar_type', 'src_id', 'tar_id'                      #
#net_pin_df: 'src', 'tar', 'src_type', 'tar_type', 'src_id', 'tar_id'                       #
#net_cell_df: 'src', 'tar', 'src_type', 'tar_type', 'src_id', 'tar_id'                      #
#cell_cell_df: 'src', 'tar', 'src_type', 'tar_type', 'src_id', 'tar_id'                     #
#edge_df: 'src_id', 'tar_id', 'e_type'                                                      #
#                             (etype: 0-p_p, 1-c_p, 2-n_p, 3-n_c, 4-c_c)                    #
#############################################################################################

if __name__ == "__main__":
  #################################################
  #parse args and import functions from CircuitOps#
  #################################################
  parser = argparse.ArgumentParser(description='path of your CircuitOps clone and the file of generate_LPG_from_tables.py')
  parser.add_argument('--path_IR', type = Path, default='../../IR_Tables/NV_NVDLA_partition_m/', action = 'store')
  parser.add_argument('--path_LPG_gen_func', type = Path, default='../../../CircuitOps/src/python/', action = 'store')
  pyargs = parser.parse_args()
  
  sys.path.append(str(pyargs.path_LPG_gen_func))
  from generate_LPG_from_tables import generate_LPG_from_tables

  ######################
  #get feature from LPG#
  ######################
  LPG, pin_df, cell_df, net_df, fo4_df, pin_pin_df, cell_pin_df, \
    net_pin_df, net_cell_df, cell_cell_df, edge_df, v_type, e_type \
    = generate_LPG_from_tables(data_root = f"{pyargs.path_IR}/")

  sys.path.remove(str(pyargs.path_LPG_gen_func))
  ### get dimensions
  N_pin, _ = pin_df.shape
  N_cell, _ = cell_df.shape
  N_net, _ = net_df.shape
  total_v_cnt = N_pin+N_cell+N_net

  N_pin_pin, _ = pin_pin_df.shape
  N_cell_pin, _ = cell_pin_df.shape
  N_net_pin, _ = net_pin_df.shape
  N_net_cell, _ = net_cell_df.shape
  N_cell_cell, _ = cell_cell_df.shape
  total_e_cnt = N_pin_pin + N_cell_pin + N_net_pin + N_net_cell + N_cell_cell
  
  #string type properties not supported
  LPG_pin_slack = LPG.new_vp("float")
  LPG_pin_slack.a[0:N_pin] = pin_df["slack"].to_numpy()

  LPG_pin_risearr = LPG.new_vp("float")
  LPG_pin_risearr.a[0:N_pin] = pin_df["risearr"].to_numpy()

  LPG_pin_cap = LPG.new_vp("float")
  LPG_pin_cap.a[0:N_pin] = pin_df["cap"].to_numpy()
  
  LPG_cell_is_seq = LPG.new_vp("bool")
  LPG_cell_is_seq.a[N_pin:N_pin+N_cell] = cell_df["is_seq"].to_numpy()

  LPG_net_net_route_length = LPG.new_vp("float")
  LPG_net_net_route_length.a[N_pin+N_cell:N_pin+N_cell+N_net] = net_df["net_route_length"].to_numpy()

  v_props = LPG.get_vertices(vprops = [LPG_pin_slack, LPG_pin_risearr, LPG_pin_cap, LPG_cell_is_seq, LPG_net_net_route_length])
  #v_props will contain the node index, pin_slack, pin_rise_arrival_time, pin_cap, cell_is_seq, net_route_length
  print("Index |       slack | rise_arrival |         cap | is_seq | route_length")
  for v_row in v_props[321:325,:]:
      print(f"{int(v_row[0]):5d} | {v_row[1]:7.4e} | {v_row[2]:12.4e} | {v_row[3]:11.4e} | {bool(v_row[4])!s:6} | {v_row[5]:7.4e}")

  print("\"is_seq\" and \"route_length\" do not have usable values since we are only printing out the pin nodes in the labeled property graph (LPG).")
