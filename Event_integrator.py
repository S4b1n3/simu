from __future__ import annotations

from component import Component, State, Port
import numpy as np
import math

class EventIntegrator(Component):

    def __init__(self, s0_time):
        Component.__init__(self, s0_time)
        self.set_outputs("sq", 0)
        self.set_inputs("sum", 0)
        self.q = 0
        self.dq = 1
        self.deltaT = s0_time
        self.deltaQ = 10**(-2)
        self.set_initial_state(S(self.deltaT, self))

class S(State):
    def __init__(self, event_time, component):
        State.__init__(self, event_time, component)

    def intern_transition(self):
        print(self.component.dq)
        self.component.q = self.component.q + self.component.deltaQ * np.sign(self.component.dq)
        self.component.deltaT = (self.component.deltaQ / abs(self.component.dq))
        self.component.transition_to(S(self.component.deltaT, self.component))

    def extern_transition(self):
        if self.component.inputs["sum"] is not None:
            self.component.q = self.component.q + self.component.inputs["sum"]
            self.component.dq = self.component.inputs["sum"]
            print("MODIF DQ",self.component.dq)
            self.component.deltaT = math.inf
            self.component.transition_to(S(self.component.deltaT, self.component))

    def output_method(self):
        temp = self.component.q + self.component.deltaQ*np.sign(self.component.dq)
        self.component.set_outputs("sq", temp)
        self.component.ports["sq"].update()

    def time_advance(self):
        pass
'''
    def conflict(self):
        print("intern transition")
        self.intern_transition()'''
