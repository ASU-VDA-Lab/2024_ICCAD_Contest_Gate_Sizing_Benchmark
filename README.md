# ICCAD_Contest_Gate_Sizing_Benchmark
This GitHub repository has the public benchmarks for the 2024 ICCAD CAD Contest Problem C for logic gate sizing, and the hidden benchmarks will be released after the contest. This contest primary goal is to explore the state-of-the-art algorithms for gate sizing to drive academic research to generate scalable gate-sizing algorithms. The secondary goal is to allow the use of a recently developed ML EDA research infrastructure which leverages [*OpenROAD's Python API*](https://github.com/The-OpenROAD-Project/OpenROAD) and [*Nvidia's CircuitOps*](https://github.com/NVlabs/CircuitOps/) data representation format for ML-EDA or GPU-accelerated EDA research. OpenROAD's Python APIs allow users to execute EDA tools with just a few lines of Python code and to access the EDA tool database directly through Python APIs, bypassing traditional file I/O. CircuitOps provides an ML-friendly data infrastructure that uses Labeled Property Graphs (LPGs) backed by Intermediate Representation (IR) Tables to create datasets for ML-EDA applications. The Python-compatible LPG minimizes the developmental effort required for ML-EDA research.


## Table of Content
  - [*IR_Tables*](./IR_Tables): Design data in CircuitOps IR tables format, units are in farad (F), Ohm (Ω), and second (s).
  - [*design*](./design): Design netlist, post-placement DEF, SDC, and reference .size output file.
  - [*platform/ASAP7*](./platform/ASAP7): ASAP7 cell library for the designs.
  - [*src*](./src)
    - [*example*](./src/example): Example scripts showing how to use OpenROAD Python API and CircuitOps LPG.
    - [*intermediate_file_generator*](./src/intermediate_file_generator): Python scripts to generate the intermediate files containing the updated timing values and capacitance values using OpenROAD after gate sizing. 
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
|        design        |   gate count   |    WNS (ns)   |    TNS (ns)   |worst slew (ns)|max load C (pF)| total leakage (uW)|
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m | 27,553| -0.595|    -156.323| 1.135| 0.061|      1.672|
| NV_NVDLA_partition_p | 79,919| -1.619|   -8,423.53| 1.627| 0.087|      5.539|
| ariane136            |143,671| -1.298| -10,143.711|  1.44| 0.072| 17,539.095|
| mempool_tile_wrap    |205,454| -1.56 | -12,697.547| 1.472| 0.072|  2,590.158|

(Reported by OpenSTA)

## Reference Sizing Result Statistics
|        design        |   gate count   |    WNS (ns)   |    TNS (ns)   |worst slew (ns)|max load C (pF)| total leakage (uW)|
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m | 27,553| -0.207|  -10.266|    NA|    NA|     2.693|
| NV_NVDLA_partition_p | 79,919| -0.226| -125.452| 0.357|    NA|     6.635|
| ariane136            |143,671| -0.214|  -27.613|  0.66|    NA| 17,545.15|
| mempool_tile_wrap    |205,454| -0.199|   -1.232| 0.857| 0.036|  2,594.44|

(Reported by OpenSTA)

## Output file format
```
<instance name> <library cell name>
<instance name> <library cell name>
<instance name> <library cell name>
...
```

## Intermediate file format
```
<pinName or portName>,<maxcap>,<maxtran>,<pin_tran>,<pin_slack>,<pin_rise_arr>,<pin_fall_arr>,<input_pin_cap>,<output_pin_cap>

<instanceName>,<staticPower>
```
("output_pin_cap" is the sum of the sink pins' capacitance and the net capacitance.)




 
