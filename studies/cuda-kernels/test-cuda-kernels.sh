#!/usr/bin/env bash

echo "Copying files"

cp standard_parallel_algorithms.h loop-dependent-variable-kernels/manual_*.cu restricted-loop-carried-array-kernels/manual_*.cu simple-reducer-kernels/manual_*.cu ../../src/cuda-kernels/
cd ../..

echo "Running setup"
python -m pip uninstall awkward_cuda_kernels && ./cuda-build.sh --install
python dev/generate-tests.py

echo "Testing"
python -m pytest -vvrs tests-cuda-kernels

echo "Cleaning up"
mv src/cuda-kernels/manual_awkward_ListArray_num.cu src/

rm src/cuda-kernels/manual* src/cuda-kernels/standard_parallel_algorithms.h

mv src/manual_awkward_ListArray_num.cu src/cuda-kernels/
