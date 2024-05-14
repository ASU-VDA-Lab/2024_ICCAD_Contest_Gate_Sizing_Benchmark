# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

### SET DESIGN ###
set DESIGN_NAME NV_NVDLA_partition_m

### SET PLATFORM ###
set PLATFORM ASAP7

### SET OUTPUT DIRECTORY ###
set OUTPUT_DIR "../../IR_Tables/${DESIGN_NAME}"

### INTERNAL DEFINTIONS: DO NOT MODIFY BELOW ####
set DESIGN_DIR "../../design/${DESIGN_NAME}"
set PLATFORM_DIR "../../platform/${PLATFORM}"

file mkdir "${OUTPUT_DIR}"

set DEF_FILE "${DESIGN_DIR}/${DESIGN_NAME}.def"
set TECH_LEF_FILE [glob ${PLATFORM_DIR}/lef/asap7_tech_1x_201209.lef]
set LEF_FILES [glob ${PLATFORM_DIR}/lef/*.lef]
set LIB_FILES [glob ${PLATFORM_DIR}/lib/*.lib]
set SDC_FILE "${DESIGN_DIR}/${DESIGN_NAME}.sdc"
set NETLIST_FILE  "${DESIGN_DIR}/${DESIGN_NAME}.v"
set SPEF_FILE "${DESIGN_DIR}/${DESIGN_NAME}.spef"

set cell_file "${OUTPUT_DIR}/cell_properties.csv"
set libcell_file "${OUTPUT_DIR}/libcell_properties.csv"
set pin_file "${OUTPUT_DIR}/pin_properties.csv"
set net_file "${OUTPUT_DIR}/net_properties.csv"
set cell_pin_file "${OUTPUT_DIR}/cell_pin_edge.csv"
set net_pin_file "${OUTPUT_DIR}/net_pin_edge.csv"
set pin_pin_file "${OUTPUT_DIR}/pin_pin_edge.csv"
set cell_net_file "${OUTPUT_DIR}/cell_net_edge.csv"
set cell_cell_file "${OUTPUT_DIR}/cell_cell_edge.csv"

