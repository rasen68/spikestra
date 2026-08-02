''' I/O handler and stuff for spikestra '''

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
        print(f"csv_to_grid: file {path} not found", file=sys.stderr)
        sys.exit(1)

    if not l or not l[0]:
        print(f"csv_to_grid: {path} csv reader was empty", file=sys.stderr)
        sys.exit(1)

    grid = Grid(len(list), len(list[0]))
    grid.load_delays(delays)
    return grid
