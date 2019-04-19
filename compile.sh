#!/usr/bin/env bash

gcc -fPIC -shared hole_filling.c -o libhf.so

python -m unittest test_hf.py

python test_runtime.py