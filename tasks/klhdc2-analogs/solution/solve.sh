#!/bin/bash
set -eu
mkdir -p /app/submission
cp /solution/run.py /app/submission/run.py
python3 /app/submission/run.py --input-dir /app/data --output-dir /app/output
