#!/usr/bin/env python3
''' Entrypoint script for spikestra '''

import sys

from grid import Grid
from wavefront import Table, propagate

def csv_to_grid(path: str) -> Grid:
    import csv

    try:
        with open(path, 'r') as f:
            reader = csv.reader(file)
            delays = list(reader)
    except FileNotFoundError:
        panic(f"csv_to_grid: file {path} not found")

    if not l or not l[0]:
        panic(f"csv_to_grid: {path} csv reader was empty")

    grid = Grid(len(list), len(list[0]))
    grid.load_delays(delays)
    return grid

def uniform_grid(n: int, m: int, delay: int) -> Grid:
    grid = Grid(n, m)
    delays = []
    for i in n:
        row = []
        for j in m:
            row.append(delay)
        delays.append(row)

    grid.load_delays(delays)
    return grid

USAGE = """spikestra.py spiking wavefront propagation algorithm
Usage:
        spikestra.py uniform rows cols delay | test with uniform grid
        spikestra.py csv path_to_csv         | use on csv of delays\
"""

def panic(string: str):
    print(string, file=sys.stderr)
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(USAGE)
    match sys.argv[1]:
        case 'uniform':
            try:
                n, m = int(sys.argv[2]), int(sys.argv[3])
                d = int(sys.argv[4])
                grid = uniform_grid(n, m, d)
                propagate(grid)
            except (IndexError, ValueError):
                panic("Usage: spikestra.py uniform rows cols delay")
        case 'csv':
            try:
                grid = csv_to_grid(sys.argv[2])
                propagate(grid)

            except IndexError:
                panic("Usage: spikestra.py csv path_to_csv")
