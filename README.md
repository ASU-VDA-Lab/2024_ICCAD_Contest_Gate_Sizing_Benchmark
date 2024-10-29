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
pip3 install torch==2.2.0
pip3 install numpy==1.24.4
pip3 install dgl==2.1.0
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
|        Design        |   Gate Count   |    WNS (ns)   |    TNS (ns)   |Total Slew Violation Difference (ns)|Total Load Capacitance Violation Difference (fF)| Total Leakage (uW)|
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m | 27,553| -0.595|    -156.323|   258.761|    256|      1.672|
| NV_NVDLA_partition_p | 79,919| -1.519|   -6,306.64| 6,125.512|  5,292|      5.539|
| ariane136            |145,776| -1.298| -10,143.711|14,843.895| 15,463| 17,539.095|
| mempool_tile_wrap    |187,851| -1.315| -10,458.099|12,069.07 | 10,779|  2,590.189|
| aes_256              |278,465| -0.284|    -212.965|    942.81|  1,300|     16.771|
| hidden1              | 38,089| -1.069|  -1,136.054| 4,073.071|  6,811|      2.762|
| hidden2              |149,396| -1.214|  -9,400.457|16,582.889| 16,661| 17,152.379|
| hidden3              |184,863| -1.563|  -2,436.288|19,755.937| 33,088| 16,513.594|
| hidden4              |260,483| -3.185| -25,334.022|19,138.199| 27,548|     21.024|
| hidden5              |283,750| -0.324|    -370.293|     3.483|     NA|     16.17 |

(Reported by OpenSTA)

## Reference Sizing Result Statistics
|        Design        |   Gate Count   |    WNS (ns)   |    TNS (ns)   |Total Slew Violation Difference (ns)|Total Load Capacitance Violation Difference (fF)| Total Leakage (uW)| Runtime (s) |
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m | 27,553| -0.207|  -10.266|       NA|       NA|     2.693|  11|
| NV_NVDLA_partition_p | 79,919| -0.126|  -17.899|    0.074|       NA|     6.635| 254|
| ariane136            |145,776| -0.214|  -27.613|   23.713|       NA|17,545.15 | 573|
| mempool_tile_wrap    |187,851| -0.191|   -2.889|   40.511|       41| 2,594.179| 489|
| aes_256              |278,465|     NA|       NA|       NA|       NA|    16.918| 501|
| hidden1              | 38,089| -0.217|  -20.302|    5.394|       NA|     2.874| 114|
| hidden2              |149,396| -0.233| -162.019|   19.842|       NA|17,156.382| 570|
| hidden3              |184,863| -0.319|   -4.742|  666.407|      480|16,514.495|2243|
| hidden4              |260,483| -0.291| -104.095|  410.963|      709|    21.904|4282|
| hidden5              |283,750|     NA|       NA|       NA|       NA|    26.831| 501|

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




 
