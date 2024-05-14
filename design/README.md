# Benchmark files
This directory contains contest benchmarks, including sdc, spef, gate-level netlist in Verilog format, and post-route def. Run the following command to unzip all files:
```
bash unzip.sh
```
## Benchmark Statistics
|        design        |   gate count   |    WNS (ps)   |    TNS (ps)   |worst slew (ps)|max load C (fF)| total leakage (uW)|
|:--------------------:|:--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
|       ariane133      | 135,062| -63,360.52| -648,873,920| 207,513.45| 29,458.64| 17,154.76702665337|
| NV_NVDLA_partition_a | 38,846| -14,052.56| -38,039,276| 37,158.04| 6,824.19| 3.1119671539785176|
| NV_NVDLA_partition_p | 78,703| -108,991.77| -527,624,288| 31,431.29| 8,170.04| 7.603496621200016|
| NV_NVDLA_partition_m | 23,513| -4,169.26| -1,144,537.12| 6,715.75| 1,688.59| 2.2363948726554853|

(Reported by OpenSTA)

## Benchmark Statistics
|        design        |   gate count   |    WNS (ps)   |    TNS (ps)   |
|:--------------------:|:--------------:|--------------:|--------------:|
|       ariane133      | 135,062| -7,431| -40,983,700|
| NV_NVDLA_partition_a | 38,846| -2,636| -6,326,200|
| NV_NVDLA_partition_p | 78,703| -2,786| -23,360,200|
| NV_NVDLA_partition_m | 23,513| -967| -209,730|

(Reported by Innovus)

