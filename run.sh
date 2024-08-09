#!/bin/bash

scripts=("sync" "transcribe insert_note")
for script in "${scripts[@]}"; do
    python -m "scripts.$script" &
done

wait
