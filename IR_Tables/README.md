# Intermediate Representation (IR) Tables
This directory contains IR Tables for CircuitOps users. Run the following command to unzip all files:
```
bash unzip.sh
```
Units are in farad (F), Ohm (Ω), and second (s)

## IR Table format
### Property Table
- Cell properties:
  - cell_name: name of the cell.
  - is_seq: 1 if is flip-flop, otherwise 0.
  - is_macro: 1 if is macro, otherwise 0.
  - is_in_clk: whether one of its pins is connected to the clock signal
  - x0: lower-left location of the cell.
  - y0: lower-let location of the cell.
  - x1: upper-right location of the cell.
  - y1: upper-right location of the cell.
  - is_buf: 1 if the cell is a buffer.
  - is_inv: 1 if the cell is an inverter.
  - libcell_name: name of the library cell.
  - cell_static_power: cell's leakage power.
  - cell_dynamic_power: sum of cell's internal and switching power.
- Pin Properties:
  - pin_name: name of the pin.
  - x: location of the pin on the x-axis.
  - y: location of the pin on the y-axis.
  - is_in_clk: whether the pin is connected to the clock signal
  - is_port: 
  - is_startpoint: 1 if the pin is the driver pin (reported by OpenSTA).
  - is_endpoint: 1 if the pin is the sink pin (reported by OpenSTA).
  - dir: 0 if it's an input of a cell, 1 if it's an output of a cell.
  - maxcap: capacitance constraint of the pin
  - maxtran: transition time constraint of the pin
  - num_reachable_endpoint: amount of connecting sink pins (reported by OpenSTA).
  - cell_name: name of the cell.
  - net_name: name of the connecting net.
  - pin_tran: pin slew.
  - pin_slack: min of the rising and falling slack.
  - pin_rise_arr: rising arrival time.
  - pin_fall_arr: falling arrival time.
  - input_pin_cap: input pin capacitance, None for output pins.
- Net Properties:
  - net_name: name of the net.
  - net_route_length: routing length of the net.
  - net_steiner_length:
  - fanout: amount of connecting sink pins.
  - total_cap: sum of the wire capacitance and the sum of sink pins' capacitance.
  - net_cap: wire capacitance.
  - net_coupling: wire coupling capacitance.
  - net_res: wire resistance.
- Libcell Properties:
  - libcell_name: name of the library cell.
  - func_id: The functional ID of a libcell is a unique identifier assigned based on its functionality. Libcells that perform the same function will share the same functional ID, while those with different functionalities will have distinct IDs.
  - libcell_area: area of the library cell.
  - worst_input_cap: maximum capacitance value across all input pins.
  - libcell_leakage: leakage power.
  - fo4_delay: the timing arc delay if the library cell is driving four of the same library cells.
  - fix_load_delay: the timing arc delay if the library cell is driving four unit inverters.
### Edge Table
- Cell-cell edge:
  - src: start.
  - tar: end.
  - src_type: indicate if the start is a cell, pin, or net.
  - tar_type: indicate if the end is a cell, pin, or net.
- Cell-net edge:
  - src: start.
  - tar: end.
  - src_type: indicate if the start is a cell, pin, or net.
  - tar_type: indicate if the end is a cell, pin, or net. 
- Cell-pin edge:
  - src: start.
  - tar: end.
  - src_type: indicate if the start is a cell, pin, or net.
  - tar_type: indicate if the end is a cell, pin, or net. 
- Net-pin edge:  
  - src: start.
  - tar: end.
  - src_type: indicate if the start is a cell, pin, or net.
  - tar_type: indicate if the end is a cell, pin, or net.
- Pin-pin edge
  - src: start.
  - tar: end.
  - src_type: indicate if the start is a cell, pin, or net.
  - tar_type: indicate if the end is a cell, pin, or net.
  - is_net: 0 indicates the pin-pin edge is inside a cell, and 1 indicates the edge is between a cell, which means it's a net.
  - arc_delay: the timing arc delay.

