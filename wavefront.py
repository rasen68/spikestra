''' Implement spiking wavefront propagation algorithm '''

from __future__ import annotations

from neuron import Neuron, Edge

class Grid:
    ''' n rows by m columns grid of neurons and edges '''
    n: int
    m: int
    grid: list[list[Neuron]]
    edges: list[Edge]

    def __init__(self, n: int, m: int) -> Grid:
        grid = []
        edges = []
        self.n = n
        self.m = m
 
        # Create grid of neurons
        for i in range(n):
            row = []
            for j in range(m):
                row.append(Neuron(i, j))
            grid.append(row)

        # Initialize east-west edges
        for j in m:
            for i in range(n-1):
                edge = Edge(grid[i][j], grid[i+1][j])
                edges.append(edge)
                bedge = Edge(grid[i+1][j], grid[i][j])
                edges.append(bedge)

        # Initialize north-south edges
        for i in n:
            for j in range(m-1):
                edge = Edge(grid[i][j], grid[i][j+1])
                edges.append(edge)
                bedge = Edge(grid[i][j+1], grid[i][j])
                edges.append(bedge)

        self.grid = grid
        self.edges = edges

    def get_neuron(self, n: int | tuple[int, int], m: int | None=None) -> Neuron:
        ''' Overloaded neuron getter, one tuple or two int arguments '''
        if m is None:
            return self.grid[n[0]][n[1]]
        else:
            return self.grid[n][m]

    def reset(self):
        [e.reset() for e in edges]
        [n.reset() for row in self.grid for n in row]
    
    def update(self):
        ''' Update edges then neurons '''
        [e.update() for e in edges]
        [n.update() for row in self.grid for n in row]

    def get_spiked(self) -> list[Neuron]:
        return [n for row in self.grid for n in row if n.spiked()]

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


type coordinate = tuple[int, int]
def propagate(grid: Grid, start: coordinate, goal: coordinate) -> Table:
    ''' Given a list of Edges between Neurons (in a grid), propagate '''
    ''' a spiking wave from start to goal and return a spike table   '''
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
