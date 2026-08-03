''' Spike table for logging events in wavefront propagation algorithm '''

from __future__ import annotations

from neuron import Neuron, coordinate

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

    def spike_time(self, c: coordinate) -> int:
        return self.first_spikes[c[0]][c[1]]

    def path(self, start: coordinate | None=None, goal: coordinate | None=None) -> list[coordinate]:
        ''' Backtrace path from goal to start (with defaults) then reverse '''
        if start is None: start = (0, 0)
        if goal is None: goal = (self.n-1, self.m-1)

        ret = [goal]
        cur = goal
        while cur != start:
            # Get adjacent neighbors
            adj = [
                (cur[0] + 1, cur[1]),
                (cur[0] - 1, cur[1]),
                (cur[0], cur[1] + 1),
                (cur[0], cur[1] - 1),
            ]

            # Remove out-of-bounds neighbors
            adj = [a for a in adj if 0 <= a[0] < self.n and 0 <= a[1] < self.m]

            # Go to neighbor with lowest first spike time
            for a in adj:
                t = self.spike_time(a)
                if t is not None and t < self.spike_time(cur):
                    cur = a
            if cur in ret:
                print("DIE DIE DIE")
                return
            ret.insert(0, cur)
        return ret
