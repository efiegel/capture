#!/bin/bash

scripts=("sync" "transcribe update_notes")
for script in "${scripts[@]}"; do
    python -m "scripts.$script" &
done

wait
