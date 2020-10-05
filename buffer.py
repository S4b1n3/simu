from component import Component, State
import math


class Buffer(Component):
    def __init__(self, s0_time):
        Component.__init__(self, s0_time)
        self._nb_jobs = 0
        self._inputs["job"] = None
        self._inputs["done"] = None
        self._outputs["req"] = None
        self.set_initial_state(Buf_a(s0_time, self))

    @property
    def nb_jobs(self):
        return self._nb_jobs

    @nb_jobs.setter
    def nb_jobs(self, new_value):
        self._nb_jobs = new_value

    def clean_inputs(self):
        print(self._inputs)
        self._inputs["job"] = None
        self._inputs["done"] = None
        print("new inputs")
        print(self._inputs)



class Buf_a(State):
    def __init__(self, event_time, component: Component):
        State.__init__(self, event_time, component)

    def extern_transition(self):
        if self.component.inputs["job"] is not None:
            self.component.nb_jobs = self.component.nb_jobs + 1
            self.component.transition_to(Buf_b(0, self.component))
        print("q = " + str(self.component.nb_jobs))

    def intern_transition(self):
        pass

    def output_method(self):
        pass

    def time_advance(self):
        pass


class Buf_b(State):
    def __init__(self, event_time, component: Component):
        State.__init__(self, event_time, component)

    def intern_transition(self):
        self.component.nb_jobs = self.component.nb_jobs - 1
        self.component.transition_to(Buf_c(math.inf, self.component))
        print("q = " + str(self.component.nb_jobs))

    def output_method(self):
        self.component.set_outputs("req", True)
        self.component.ports["req"].update()

    def extern_transition(self):
        if self.component.inputs["job"] is not None:
            self.component.nb_jobs = self.component.nb_jobs + 1
            self.component.transition_to(Buf_b(0, self.component))
        print("q = " + str(self.component.nb_jobs))

    def time_advance(self):
        pass


class Buf_c(State):
    def __init__(self, event_time, component):
        State.__init__(self, event_time, component)

    def extern_transition(self):
        if self.component.inputs["job"] is not None:
            self.component.nb_jobs = self.component.nb_jobs + 1
            self.component.transition_to(Buf_c(math.inf, self.component))
        elif self.component.inputs["done"] is not None:
            if self.component.nb_jobs > 0:
                self.component.transition_to(Buf_b(0, self.component))
            elif self.component.nb_jobs == 0:
                self.component.transition_to(Buf_a(math.inf, self.component))
        print("q = " + str(self.component.nb_jobs))

    def intern_transition(self):
        print("q = " + str(self.component.nb_jobs))

    def output_method(self):
        pass

    def time_advance(self):
        pass
