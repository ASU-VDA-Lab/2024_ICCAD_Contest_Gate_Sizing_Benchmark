# Script for evaluating and checking the validity of the sizing results
This directory contains evaluation scripts for the contest and the evaluation method for users of the OpenROAD Python API. The evaluation penalties are set to 1 for this sample evaluation script. All penalties are subject to change during the alpha submission, beta submission, and final evaluation stages. The run-time penalty is not included in this sample evaluation script.

## Run evaluation
(Make sure you have OpenROAD built locally)
Run the following command to check the correctness of the gate sizing result and get the sample score:
- Add the path to your output file with the "--file_path" flag.
- Add the name of the corresponding benchmark you want to evaluate with the "--design_name" flag
```
# Add --dump_def flag to dump the updated def file
../../OpenROAD/build/src/openroad -python evaluation.py --file_path <Path to your output file> --design_name <The name of the benchmark>
```

## Importable functions for OpenROAD Python API users
Participants using OpenROAD Python APIs to modify gate sizes in the OpenROAD database directly can integrate the evaluation function into their Python code. Please add the following scripts to your Python code:
- "check_validity_OpenROAD" checks the validity of your sizing result, and takes the following arguments:
  - designName: the name of the benchmark.
  - design: the openroad.Design object. Please check out [*the example*](https://github.com/ASU-VDA-Lab/2024_ICCAD_Contest_Gate_Sizing_Benchmark/tree/main/src/example) to see how to get it.
  - timing: the openroad.Timing object. Please check out [*the example*](https://github.com/ASU-VDA-Lab/2024_ICCAD_Contest_Gate_Sizing_Benchmark/tree/main/src/example) to see how to get it.
- "ICCAD_evaluation_OpenROAD" runs the validity checking and calculates a sample evaluation score. It takes the following arguments:
  - designName: the name of the benchmark.
  - design: the openroad.Design object. Please check out [*the example*](https://github.com/ASU-VDA-Lab/2024_ICCAD_Contest_Gate_Sizing_Benchmark/tree/main/src/example) to see how to get it.
  - timing: the openroad.Timing object. Please check out [*the example*](https://github.com/ASU-VDA-Lab/2024_ICCAD_Contest_Gate_Sizing_Benchmark/tree/main/src/example) to see how to get it.
```
import sys
sys.path.append(<path to the src directory>)
from evaluation import check_validity_OpenROAD, ICCAD_evaluation_OpenROAD
```
Please check [*evaluation_OpenROAD.py*](./evaluation_OpenROAD.py) and [*check_validity_OpenROAD.py*](./check_validity_OpenROAD.py) for more details.
