# Benchmark files
This directory contains contest benchmarks, including sdc, spef, gate-level netlist in Verilog format, and post-route def. Run the following command to unzip all files:
```
bash unzip.sh
```
## Benchmark Statistics
|        design        |   gate count   |    WNS (ps)   |    TNS (ps)   |worst slew (ps)|max load C (fF)| total leakage (uW)|
|:--------------------:|:--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_a | 38,846| -14052.56| -38039276| 37158.04| 6824.19| 3.1119671539785176|
| NV_NVDLA_partition_p | 78,703| -108991.77| -527624288| 31431.29| 8170.04| 7.603496621200016|
| NV_NVDLA_partition_m | 23,513| -4169.26| -1144537.12| 6715.75| 1688.59| 2.2363948726554853|

(Reported by OpenSTA)

## Benchmark Statistics
|        design        |   gate count   |    WNS (ps)   |    TNS (ps)   |
|:--------------------:|:--------------:|--------------:|--------------:|
| NV_NVDLA_partition_a | 38,846| -2636| -6326200|
| NV_NVDLA_partition_p | 78,703| -2786| -23360200|
| NV_NVDLA_partition_m | 23,513| -967| -209730|

(Reported by Innovus)

