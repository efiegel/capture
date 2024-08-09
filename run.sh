#!/bin/bash

scripts=("sync" "transcribe")
for script in "${scripts[@]}"; do
    python -m "scripts.$script" &
done

wait
