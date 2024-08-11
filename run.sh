#!/bin/bash

cleanup() {
    pkill -P $$
    exit 0
}

trap cleanup SIGINT

scripts=("sync" "transcribe" "update_notes")
for script in "${scripts[@]}"; do
    python -m "scripts.$script" &
done

wait
