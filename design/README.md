# Benchmark files
This directory contains contest benchmarks, including sdc, gate-level netlist in Verilog format, post-placement def, and reference .size output file. Run the following command to unzip all files:
```
bash unzip.sh
```
## Benchmark Statistics
|        design        |   gate count   |    WNS (ns)   |    TNS (ns)   |worst slew (ns)|max load C (pF)| total leakage (uW)|
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m | 27,553| -0.595|    -156.323| 1.135| 0.061|      1.672|
| NV_NVDLA_partition_p | 79,919| -1.619|   -8,423.53| 1.627| 0.087|      5.539|
| ariane136            |145,776| -1.298| -10,143.711|  1.44| 0.072| 17,539.095|
| mempool_tile_wrap    |187,851| -1.56 | -12,697.547| 1.472| 0.072|  2,590.158|

(Reported by OpenSTA)

## Reference Sizing Result Statistics
|        design        |   gate count   |    WNS (ns)   |    TNS (ns)   |worst slew (ns)|max load C (pF)| total leakage (uW)|
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m | 27,553| -0.207|  -10.266|    NA|    NA|     2.693|
| NV_NVDLA_partition_p | 79,919| -0.226| -125.452| 0.357|    NA|     6.635|
| ariane136            |145,776| -0.214|  -27.613|  0.66|    NA| 17,545.15|
| mempool_tile_wrap    |187,851| -0.199|   -1.232| 0.857| 0.036|  2,594.44|

(Reported by OpenSTA)


