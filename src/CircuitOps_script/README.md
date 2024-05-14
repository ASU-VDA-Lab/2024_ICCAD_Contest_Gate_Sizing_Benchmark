# CircuitOps script for ICCAD 2024 CAD Contest benchmarks
This directory contains [*OpenROAD*](https://github.com/The-OpenROAD-Project/OpenROAD/tree/master) scripts to generate the CircuitOps Intermediate Representation (IR) Tables.

## Run the script
Make sure you have OpenROAD built locally.
Please modify the relative path and the "DESIGN_NAME" variable in [*ICCAD_set_design.tcl*](./ICCAD_set_design.tcl) before running the script
Run the following command to generate the new IR Tables:
```
../../OpenROAD/build/src/openroad ICCAD_generate_tables.tcl
```
