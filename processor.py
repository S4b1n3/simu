from component import Component, State
import math


class Processor(Component):
    def __init__(self, s0_time):
        Component.__init__(self, s0_time)
        self.set_inputs("req", None)
        self.set_outputs("done", None)
        self.set_initial_state(Proc_idle(s0_time, self))

    def clean_inputs(self):
        self.set_inputs("req", None)


class Proc_idle(State):
    def __init__(self, event_time, component: Component):
        State.__init__(self, event_time, component)

    def intern_transition(self):
        pass

    def output_method(self):
        pass

    def time_advance(self):
        pass

    def extern_transition(self):
        if self.component.inputs["req"] is not None:
            self.component.transition_to(Proc_busy(3, self.component))


class Proc_busy(State):
    def __init__(self, event_time, component: Component):
        State.__init__(self, event_time, component)

    def intern_transition(self):
        self.component.transition_to(Proc_idle(math.inf, self.component))

    def output_method(self):
        self.component.set_outputs("done", True)
        self.component.ports["done"].update()

    def time_advance(self):
        pass

    def extern_transition(self):
        pass
