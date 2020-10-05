from __future__ import annotations

from component import Component, State, Port


class Generator(Component):

    def __init__(self, s0_time):
        Component.__init__(self, s0_time)
        self.set_outputs("job", None)
        self.set_initial_state(Gen_SO(s0_time, self))


class Gen_SO(State):
    def __init__(self, event_time, component):
        State.__init__(self, event_time, component)

    def intern_transition(self):
        self.component.transition_to(Gen_SO(2, self.component))


    def extern_transition(self):
        pass

    def output_method(self):
        self.component.set_outputs("job", True)
        self.component.ports["job"].update()

    def time_advance(self):
        pass
