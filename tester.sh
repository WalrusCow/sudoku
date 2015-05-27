#!/bin/bash

set -m

for i in $(seq 1 5); do
  for j in $(seq 1 4); do
    { time python sudoku.py $1 |tail -1 >> "$1 nodes".txt ; } 2>&1 | tail -3 | head -1 >> "$1 times".txt &
  done
  # Wait for threads
  while [ 1 ]; do fg 2> /dev/null; [ $? == 1 ] && break; done
done
