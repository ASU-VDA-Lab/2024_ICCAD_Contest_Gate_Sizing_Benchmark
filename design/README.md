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

