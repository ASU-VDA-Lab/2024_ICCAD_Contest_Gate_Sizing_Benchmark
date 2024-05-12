# OpenROAD Python API and Nvidia's CircuitOps example
This directory contains sample Python scripts for using [*OpenROAD Python APIs*](https://github.com/The-OpenROAD-Project/OpenROAD/tree/master) and [*Nvidia's CircuitOps*](https://github.com/NVlabs/CircuitOps/tree/main).

## Nvidia's CircuitOps example
Run the following command to run the example script to build the LPG using IR Tables:
```
python3 CircuitOps_example.py
```
For more examples, please find [*NVlabs/CircuitOps/src/python*](https://github.com/NVlabs/CircuitOps/tree/main/src/python) and [*ASU-VDA-Lab/ASP-DAC24-Tutorial*](https://github.com/ASU-VDA-Lab/ASP-DAC24-Tutorial/tree/main).

## OpenROAD Python API
(Make sure to build OpenROAD locally first or use the provided Dockerfile to build the environment)
Run the following command to run the example script:
```
../../OpenROAD/build/src/openroad -python OpenROAD_example.py
```
For more examples, please find [*ASU-VDA-Lab/ASP-DAC24-Tutorial*](https://github.com/ASU-VDA-Lab/ASP-DAC24-Tutorial/tree/main).
