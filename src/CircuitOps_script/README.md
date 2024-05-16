# CircuitOps script for ICCAD 2024 CAD Contest benchmarks
This directory contains Python scripts that generate updated timing values after gate sizing, following the CircuitOps Intermediate Representation (IR) Tables format.

## Run the script
Make sure you have OpenROAD built locally. Run the following command to get the updated timing values:
```
# You can also import the "updated_dataframe_generate" function from the Python file to get the pandas DataFrame
../../OpenROAD/build/src/openroad update_circuitops_properties.py --design_name <design name> --file_path <output file> --dump_csv
```
