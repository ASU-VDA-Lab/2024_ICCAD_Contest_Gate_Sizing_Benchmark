# ICCAD_Contest_Gate_Sizing_Benchmark
This GitHub repository has the public benchmarks for the 2024 ICCAD CAD Contest Problem C, and the hidden benchmarks will be released after the contest. This contest aims to explore the state-of-the-art algorithms for gate sizing to drive academic research to generate scalable gate-sizing algorithms and have people get hands-on with [*OpenROAD's Python API*](https://github.com/The-OpenROAD-Project/OpenROAD) and [*Nvidia's CircuitOps*](https://github.com/NVlabs/CircuitOps/) data representation format for ML-EDA or GPU-accelerated EDA research. OpenROAD's Python APIs allow users to execute EDA tools with just a few lines of Python code and to access the EDA tool database directly through Python APIs, bypassing traditional file I/O. CircuitOps provides an ML-friendly data infrastructure that uses Labeled Property Graphs (LPGs) backed by Intermediate Representation (IR) Tables to create datasets for ML-EDA applications. The Python-compatible LPG minimizes the developmental effort required for ML-EDA research."


## Table of Content
  - [*IR_Tables*](./IR_Tables): Design data in CircuitOps IR Table format.
  - [*design*](./design): Design netlist, post-routed DEF, SDC, and SPEF file.
  - [*platform/ASAP7*](./platform/ASAP7): ASAP7 cell library for the designs.
  - [*src*](./src)
    - [*example*](./src/example): Example scripts showing how to use OpenROAD Python API and CircuitOps LPG.
    - [*CircuitOps_script*](./src/CircuitOps_script): CircuitOps scripts to generate new IR Tables.
    - [*evaluation*](./src/evaluation): Evaluation scripts for the contest and the evaluation method for users of the OpenROAD Python API.
## Materials for using OpenROAD's Python API and Nvidia's CircuitOps
  - R. Liang, A. Agnesina, G. Pradipta, V. A. Chhabria and H. Ren, "Invited Paper: CircuitOps: An ML Infrastructure Enabling Generative AI for VLSI Circuit Optimization," in ICCAD, 2023
    - [CircuitOps: An ML Infrastructure Enabling Generative AI for VLSI Circuit Optimization](https://ieeexplore.ieee.org/abstract/document/10323611)
  - V. A. Chhabria, W. Jiang, A. B. Kahng, R. Liang, H. Ren, S. S. Sapatnekar and B.-Y. Wu, "OpenROAD and CircuitOps: Infrastructure for ML EDA Research and Education," in VTS, 2024
    - [OpenROAD and CircuitOps: Infrastructure for ML EDA Research and Education](https://vlsicad.ucsd.edu/Publications/Conferences/407/c407.pdf)
  - CircuitOps and OpenROAD Python API Tutorial at ASP-DAC 2024
    - [ASU-VDA-Lab/ASP-DAC24-Tutorial](https://github.com/ASU-VDA-Lab/ASP-DAC24-Tutorial)
  - OpenROAD github repository
    - [The-OpenROAD-Project/OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD)
  - CircuitOps github repository
    - [NVlabs/CircuitOps](https://github.com/NVlabs/CircuitOps/)

## Build OpenROAD and CircuitOps

###  Option 1: Build using Docker 
The following technique assumes you have docker installed on your machine. You can install docker from [here](https://docs.docker.com/engine/install/). Build the docker image and run using the following commands:
```
docker build -t <image_name> .
docker run -it --name <container_name> <image_name>
```

### Option 2: Build locally
The following technique assumes you have a machine with the required Ubuntu OS prerequisite of OpenROAD and CircuitOps.

Install dependencies for OpenROAD:
```
sudo ./OpenROAD/etc/DependencyInstaller.sh
```

Install dependencies for CircuitOps and ML EDA applications:
```
sudo apt-get install -y python3-matplotlib
sudo apt-get install -y nvidia-cuda-toolkit
sudo apt-get update
sudo apt-get install -y python3-graph-tool
sudo apt-get update && apt-get install -y gnupg2 ca-certificates
sudo apt-get install -y python3-pip
pip3 install torch
pip3 install dgl
pip3 install pycairo
pip3 install pandas
pip3 install scikit-learn
```

Once packages have been installed, build OpenROAD:

```
cd ./OpenROAD/
mkdir build
cd build
cmake ..
make -j
```

## Benchmark Statistics
|        design        |   gate count   |    WNS (ps)   |    TNS (ps)   |worst slew (ps)|max load C (fF)| total leakage (uW)|
|:--------------------:|:--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_a | 38846| -14052.56| -38039276| 37158.04| 6824.19| 3.1119671539785176|
| NV_NVDLA_partition_p | 78703| -108991.77| -527624288| 31431.29| 8170.04| 7.603496621200016|
| NV_NVDLA_partition_m | 23513| -4169.26| -1144537.12| 6715.75| 1688.59| 2.2363948726554853|

(Reported by OpenSTA)

## Benchmark Statistics
|        design        |   gate count   |    WNS (ps)   |    TNS (ps)   |
|:--------------------:|:--------------:|--------------:|--------------:|
| NV_NVDLA_partition_a | 38846| -2636| -6326200|
| NV_NVDLA_partition_p | 78703| -2786| -23360200|
| NV_NVDLA_partition_m | 23513| -967| -209730|

(Reported by Innovus)

## Output file format
```
<instance name> <library cell name>
<instance name> <library cell name>
<instance name> <library cell name>
...
```

## Q&A
- Q1: Does the cell library provide the area information?
- A1: Yes, you can find the area information in the lib files.




 
