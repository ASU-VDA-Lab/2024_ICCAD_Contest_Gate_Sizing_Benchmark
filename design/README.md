# Benchmark files
This directory contains contest benchmarks, including sdc, gate-level netlist in Verilog format, post-placement def, and reference .size output file. Run the following command to unzip all files:
```
bash unzip.sh
```
## Benchmark Statistics
|        Design        |   Gate Count   |    WNS (ns)   |    TNS (ns)   |Total Slew Violation Difference (ns)|Total Load Capacitance Violation Difference (fF)| Total Leakage (uW)|
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m | 27,553| -0.595|    -156.323|   258.761|    256|      1.672|
| NV_NVDLA_partition_p | 79,919| -1.519|   -6,306.64| 6,125.512|  5,292|      5.539|
| ariane136            |145,776| -1.298| -10,143.711|14,843.895| 15,463| 17,539.095|
| mempool_tile_wrap    |187,851| -1.315| -10,458.099|12,069.07 | 10,779|  2,590.189|
| aes_256              |278,465| -0.284|    -212.965|    942.81|  1,300|     16.771|

(Reported by OpenSTA)

## Reference Sizing Result Statistics
|        Design        |   Gate Count   |    WNS (ns)   |    TNS (ns)   |Total Slew Violation Difference (ns)|Total Load Capacitance Violation Difference (fF)| Total Leakage (uW)| Runtime (s) |
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m | 27,553| -0.207|  -10.266|    NA|    NA|     2.693| 11|
| NV_NVDLA_partition_p | 79,919| -0.126|  -17.899| 0.074|    NA|     6.635|254|
| ariane136            |145,776| -0.214|  -27.613|23.713|    NA|17,545.15 |573|
| mempool_tile_wrap    |187,851| -0.191|   -2.889|40.511|    41| 2,594.179|489|
| aes_256              |278,465|     NA|       NA|    NA|    NA|    16.918|501|

(Reported by OpenSTA)

