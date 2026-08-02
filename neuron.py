''' Spiking neurons and edges between them '''

from __future__ import annotations

type coordinate = tuple[int, int]

class Neuron:
    ''' Stateful Neuron model with membrane and recovery '''
    c: coordinate
    _I: int # synaptic input
    _v: int # potential
    _u: int # recovery
    edges_in: list[Edge]
    edges_out: list[Edge]

    def __init__(self, c: coordinate) -> Neuron:
        self.c = c
        self.edges_in = []
        self.edges_out = []
        self.reset()

    def update(self):
        ''' computes u(t+1), v(t+1) based on equations 2.1 and 2.2       '''
        ''' call after self.I is loaded with input from Edges this is in '''
        v, u = self._v, self._u # old values
        self._v = u + self.I
        self._u = -5 if v == 1 else min(u + 1, 0)
        self._I = 0 # reset

    def spiked(self) -> bool:
        return self._v >= 1

    def increment(self):
        self._I += 1

    def reset(self):
        self._I = 0
        self._v = 0
        self._u = 0

class Edge:
    ''' An Edge is a path between two neurons, from j to i '''
    ''' When j spikes, load i's input I                    '''
    i: Neuron
    j: Neuron
    D: int # axonal delay
    _d: int # delay counter

    def __init__(self, i: Neuron, j: Neuron, D: int) -> Edge:
        self.i = i
        self.j = j
        self.D = D
        self.reset()
        self.i.edges_in.append(self)
        self.j.edges_out.append(self)

    def update(self):
        # Update i.I based on equation 2.3
        # Together, the Edges containing i will create the sum
        # and i's update() reset i.I after each time step
        if self._d == 1:
            self.i.increment()

        # Update d based on j.v and equation 2.4
        self._d = self.D if self.j.spiked() else max(self._d - 1, 0)

    def reset(self):
        self._d = 0
