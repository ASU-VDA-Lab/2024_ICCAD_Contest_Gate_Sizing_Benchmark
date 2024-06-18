# OpenROAD Python API and Nvidia's CircuitOps example
This directory contains sample Python scripts for using [*OpenROAD Python APIs*](https://github.com/The-OpenROAD-Project/OpenROAD/tree/master) and [*Nvidia's CircuitOps*](https://github.com/NVlabs/CircuitOps/tree/main).

## Nvidia's CircuitOps example
Run the following command to run the example script to build the Labeled Property Graph (LPG) using Intermediate Representation (IR) Tables:

- Add the path to the directory containing IR Tables with the "--path_IR" flag.
- Add the path to the directory containing the LPG creation function using the "--path_LPG_gen_func" flag. The function is defined [*here*](https://github.com/NVlabs/CircuitOps/blob/main/src/python/generate_LPG_from_tables.py), and it takes the path to the IR Table as an argument.
```
python3 CircuitOps_example.py --path_IR ../../IR_Tables/NV_NVDLA_partition_m/ --path_LPG_gen_func ../../CircuitOps/src/python/
```
For more examples, please find [*NVlabs/CircuitOps/src/python*](https://github.com/NVlabs/CircuitOps/tree/main/src/python) and [*ASU-VDA-Lab/ASP-DAC24-Tutorial*](https://github.com/ASU-VDA-Lab/ASP-DAC24-Tutorial/tree/main).

## OpenROAD Python API
(Make sure to build OpenROAD locally first or use the provided Dockerfile to build the environment)
Run the following command to execute the example script:
- Replace "The name of the benchmark" with the name of the provided benchmark. The default benchmark is NV_NVDLA_partition_m if the "--design_name" flag is not added.
```
../../OpenROAD/build/src/openroad -python OpenROAD_example.py --design_name <The name of the benchmark>
```
For more examples, please find [*ASU-VDA-Lab/ASP-DAC24-Tutorial*](https://github.com/ASU-VDA-Lab/ASP-DAC24-Tutorial/tree/main).
