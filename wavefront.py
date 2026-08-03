''' Implement spiking wavefront propagation algorithm '''

from __future__ import annotations

from neuron import coordinate
from grid import Grid
from table import Table

def propagate(grid: Grid, start: coordinate | None=None, goal: coordinate | None=None) -> Table:
    ''' Given a grid loaded with delays, propagate a spiking '''
    ''' wave from start to goal and return a spike table     '''
    if start is None: start = (0, 0)
    if goal is None: goal = (grid.n-1, grid.m-1)

    grid.reset()
    time = 0
    table = Table(grid.n, grid.m)
    s = grid.get_neuron(start)
    g = grid.get_neuron(goal)

    # Start wavefront by spiking s
    s.force_spike()
    table.append(time, s)
    # Timestep until g spikes
    while not g.spiked():
        time += 1
        grid.update()
        for neuron in grid.get_spiked():
            table.append(time, neuron)

    print("Goal neuron spiked at time t =", time)
    print("Total spikes:", len(table.entries))
    return table
