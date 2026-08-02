''' Implement spiking wavefront propagation algorithm '''

from __future__ import annotations

from neuron import Neuron, coordinate
from grid import Grid

class Table:
    times: list[int]
    neurons: list[Neuron] # can have repeats
    entries: list[tuple[int, Neuron]]

    def __init__(self) -> Table:
        self.times = []
        self.neurons = []
        self.entries = []

    def append(self, time: int, neuron: Neuron):
        self.times.append(time)
        self.neurons.append(neuron)
        self.entries.append((time, neuron))

    def print(self):
        for t, n in zip(self.times, self.neurons)
            print(f"Time: {t}\t\tNeuron: {n.c}")


def propagate(grid: Grid, start: coordinate | None, goal: coordinate | None) -> Table:
    ''' Given a grid loaded with delays, propagate a spiking '''
    ''' wave from start to goal and return a spike table     '''
    if start is None: start = (0, 0)
    if goal is None: goal = (grid.n, grid.m)

    grid.reset()
    time = 1
    table = Table()
    s = grid.get(start)
    g = grid.get(goal)

    # Start wavefront by spiking s
    s.force_spike()
    table.append(time, s)

    # Timestep until g spikes
    while not g.spiked():
        time += 1
        grid.update()
        for neuron in grid.get_spiked():
            table.append(time, neuron)

    return table
