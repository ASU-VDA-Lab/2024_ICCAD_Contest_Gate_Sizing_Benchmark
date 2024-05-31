# Benchmark files
This directory contains contest benchmarks, including sdc, spef, gate-level netlist in Verilog format, and post-route def. Run the following command to unzip all files:
```
bash unzip.sh
```
## Benchmark Statistics
|        design        |   gate count   |    WNS (ns)   |    TNS (ns)   |worst slew (ns)|max load C (pF)| total leakage (uW)|
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m |          23,856|         -0.631|       -178.580|          1.186|          0.063|          1.527|

(Reported by OpenSTA)

## Reference Sizing Result Statistics
|        design        |   gate count   |    WNS (ns)   |    TNS (ns)   |worst slew (ns)|max load C (pF)| total leakage (uW)|
|:--------------------:|---------------:|--------------:|--------------:|--------------:|--------------:|--------------:|
| NV_NVDLA_partition_m |          23,856|         -0.202|         -9.088|          0.255|          0.015|          2.309|

(Reported by OpenSTA)

