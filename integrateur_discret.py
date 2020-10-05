from __future__ import annotations

from component import Component, State, Port


class Integrator(Component):

    def __init__(self, s0_time):
        Component.__init__(self, s0_time)
        self.set_outputs("sx", 0)
        self.set_inputs("sum", 0)
        self.set_initial_state(S(s0_time, self))
        self.x = 0
        self.dx = 0
        self.hstep = s0_time


class S(State):
    def __init__(self, event_time, component):
        State.__init__(self, event_time, component)

    def intern_transition(self):
        print(self.component.dx)
        self.component.x = self.component.x + self.component.dx * self.component.hstep
        self.component.transition_to(S(self.component.hstep, self.component))

    def extern_transition(self):
        if self.component.inputs["sum"] is not None:
            self.component.x = self.component.inputs["sum"]

    def output_method(self):
        self.component.set_outputs("sx", self.component.x)
        self.component.ports["sx"].update()

    def time_advance(self):
        pass
