''' Spiking neurons and edges between them '''

from __future__ import annotations

class Neuron:
    ''' Stateful Neuron model with membrane and recovery '''
    c: tuple[int, int] # coordinate position
    I: int # synaptic input
    v: int # potential
    u: int # recovery

    def __init__(self, coordinate: tuple[int, int]) -> Neuron:
        self.c = coordinate
        self.I = 0
        self.v = 0
        self.u = 0

    def update(self):
        ''' computes u(t+1), v(t+1) based on equations 2.1 and 2.2       '''
        ''' call after self.I is loaded with input from Edges this is in '''
        v, u = self.v, self.u # old values
        self.v = u + self.I
        if v == 1:
            self.u = -5
        else:
            self.u = min(u + 1, 0)
        self.I = 0 # reset 

    def spiked(self) -> bool:
        return self.v >= 1

class Edge:
    ''' An Edge is a path between two neurons, from j to i '''
    ''' When j spikes, load i's input I                    '''
    i: Neuron
    j: Neuron
    D: int # axonal delay
    d: int # delay counter

    def __init__(self, i: Neuron, j: Neuron, D: int) -> Edge:
        self.i = i
        self.j = j
        self.D = D
        self.d = 0

    def update(self):
        # Update i.I based on equation 2.3
        # Together, the Edges containing i will create the sum
        # and i's update() reset i.I after each time step
        if self.d == 1:
            self.i.I += 1

        # Update d based on j.v and equation 2.4
        if self.j.spiked():
            self.d = self.D
        else:
            self.d = max(self.d - 1, 0)
