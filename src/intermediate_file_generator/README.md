# Intermediate file generator for ICCAD 2024 CAD Contest benchmarks
This directory contains Python scripts that generate updated timing values after gate sizing, following the CircuitOps Intermediate Representation (IR) Tables format.

## Run the script
Make sure you have OpenROAD built locally. Run the following command to get the updated timing values:
- Add the name of the benchmark with the "--design_name" flag.
- Add the path including the name of your output file with the "--file_path" flag.
- Add the "--dump_csv" flag to get the intermediate files.
  - Add the output directory with the "--dump_path" flag if "--dump_csv" flag is added.
```
# You can also import the "updated_dataframe_generate" function from the Python file to get the pandas DataFrame
../../OpenROAD/build/src/openroad update_circuitops_properties.py --design_name <design name> --file_path <output file> --dump_csv --dump_path ./
```

## Intermediate file format
```
<pinName or portName>,<maxcap>,<maxtran>,<pin_tran>,<pin_slack>,<pin_rise_arr>,<pin_fall_arr>,<input_pin_cap>,<output_pin_cap>

<instanceName>,<staticPower>
```
"output_pin_cap" is the sum of the sink pins' capacitance. You can get it by subtracting the "total_cap" with "net_cap" from the net properties IR Table.
