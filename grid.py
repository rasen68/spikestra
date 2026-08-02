''' Grid of Neurons and Edges for wavefront to propagate through '''

from __future__ import annotations

from neuron import Neuron, Edge, coordinate

class Grid:
    ''' n rows by m columns grid of neurons and edges        '''
    ''' Does not keep track of time, that is algorithm's job '''
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

    def get_neuron(self, n: int | coordinate, m: int | None=None) -> Neuron:
        ''' Overloaded neuron getter, one tuple or two int arguments '''
        if m is None:
            return self.grid[n[0]][n[1]]
        else:
            return self.grid[n][m]

    def reset(self):
        ''' Reset grid by resetting all neurons '''
        [e.reset() for e in edges]
        [n.reset() for row in self.grid for n in row]
    
    def update(self):
        ''' Update edges then neurons '''
        [e.update() for e in edges]
        [n.update() for row in self.grid for n in row]

    def get_spiked(self) -> list[Neuron]:
        ''' Returns all neurons that have spiked this time step '''
        return [n for row in self.grid for n in row if n.spiked()]
