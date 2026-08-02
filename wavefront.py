''' Implement spiking wavefront propagation algorithm '''

from __future__ import annotations

from neuron import Neuron, coordinate
from grid import Grid

class Table:
    n: int # rows
    m: int # cols
    times: list[int]
    neurons: list[Neuron] # can have repeats
    entries: list[tuple[int, Neuron]]
    first_spikes: list[list[int | None]]

    def __init__(self, n: int, m: int) -> Table:
        self.n = n
        self.m = m
        self.times = []
        self.neurons = []
        self.entries = []
        self.first_spikes = [[None for i in range(n)] for i in range(m)]

    def append(self, time: int, neuron: Neuron):
        self.times.append(time)
        self.neurons.append(neuron)
        self.entries.append((time, neuron))

        i, j = neuron.c
        if self.first_spikes[i][j] is None:
            self.first_spikes[i][j] = time

    def print(self):
        for t, n in zip(self.times, self.neurons):
            print(f"Time:  {t}\tNeuron: {n.c}")


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
