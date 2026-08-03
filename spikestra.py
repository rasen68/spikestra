#!/usr/bin/env python3
''' Entrypoint script for spikestra '''

import sys

from grid import Grid
from neuron import coordinate
from table import Table
from wavefront import propagate

def csv_to_grid(path: str) -> Grid:
    import csv

    try:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            delays = list(reader)
    except FileNotFoundError:
        panic(f"csv_to_grid: file {path} not found")

    if not delays or not delays[0]:
        panic(f"csv_to_grid: {path} csv reader was empty")

    delays = [[int(x) for x in row] for row in delays]
    grid = Grid(len(delays), len(delays[0]))
    grid.load_delays(delays)
    return grid

def uniform_grid(n: int, m: int, delay: int) -> Grid:
    grid = Grid(n, m)
    delays = []
    for i in range(n):
        row = []
        for j in range(m):
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

def display(c: coordinate) -> coordinate:
    ''' convert to 1-indexed coords for output '''
    return (c[0] + 1, c[1] + 1)

def print_table(table: Table):
    for t, n in zip(table.times, table.neurons):
        print(f"Time:  {t}\tNeuron: {display(n.c)}")

def heatmap(table: Table, path: bool=False):
    ''' heatmap of first spike times with shortest path overlaid '''
    import matplotlib.pyplot as plt
    import numpy as np

    data = np.array(
        [[np.nan if t is None else t for t in row] for row in table.first_spikes],
        dtype=float,
    )

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='viridis', origin='upper')
    fig.colorbar(im, ax=ax, label='first spike time')

    # 1-indexed tick labels; imshow positions stay 0-based
    ax.set_xticks(range(table.m))
    ax.set_yticks(range(table.n))
    ax.set_xticklabels(range(1, table.m + 1))
    ax.set_yticklabels(range(1, table.n + 1))

    if path:
        rows, cols = zip(*table.path())  # (i, j) -> y, x for imshow
        ax.plot(cols, rows, color='red', linewidth=2, markersize=4)
        ax.plot(cols[0], rows[0], 'go', markersize=8)   # start
        ax.plot(cols[-1], rows[-1], 'rs', markersize=8)  # goal

    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        panic(USAGE)

    # Get grid based on subcmd
    match sys.argv[1]:
        case 'uniform':
            try:
                n, m = int(sys.argv[2]), int(sys.argv[3])
                d = int(sys.argv[4])
                grid = uniform_grid(n, m, d)
            except (IndexError, ValueError):
                panic("Usage: spikestra.py uniform rows cols delay")
        case 'csv':
            try:
                grid = csv_to_grid(sys.argv[2])
            except IndexError:
                panic("Usage: spikestra.py csv path_to_csv")
        case _:
            panic(USAGE)

    # Propagate spiking wavefront and report output
    table = propagate(grid)

    print("\nSpike table:")
    print_table(table)

    print("\nShortest path:")
    print([display(c) for c in table.path()])

    print("\nFirst spike time heatmap:")
    heatmap(table)
    heatmap(table, True)
