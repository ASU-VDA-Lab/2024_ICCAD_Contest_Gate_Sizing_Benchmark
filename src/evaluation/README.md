# Script for evaluating and checking the validity of the sizing results
This directory contains evaluation scripts for the contest and the evaluation method for users of the OpenROAD Python API.

## Run evaluation
(Make sure you have OpenROAD built locally)
Run the following command to check the correctness of the gate sizing result and get the sample score:
```
# Add --dump_def flag to dump the updated def file
../../OpenROAD/build/src/openroad -python evaluation.py --file_path <Path to your output file> --design_name <The name of the benchmark>
```

## Importable functions for OpenROAD Python API users
Please add the following scripts to your Python code:
```
import sys
sys.path.append(<path to the src directory>)
from evaluation import check_validity_OpenROAD, ICCAD_evaluation_OpenROAD
```
Please check [*evaluation_OpenROAD.py*](./evaluation_OpenROAD.py) and [*check_validity_OpenROAD.py*](./check_validity_OpenROAD.py) for more details.
