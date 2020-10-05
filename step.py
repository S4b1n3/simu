from component import Component, State
import math


class Step(Component):
    def __init__(self, s0_time, xi, xf, nameOfOutput):
        Component.__init__(self, 0)
        self._outputs[nameOfOutput] = None
        self._myOutput = nameOfOutput
        self._xi = xi
        self._xf = xf
        self._timeBeforeStep = s0_time
        self.set_initial_state(First_state(0, self))

    @property
    def myOutput(self):
        return self._myOutput

    @property
    def timeBeforeStep(self):
        return self._timeBeforeStep

    @property
    def xi(self):
        return self._xi

    @xi.setter
    def xi(self, value):
        self._xi = value

    @property
    def xf(self):
        return self._xf

    @xf.setter
    def xf(self, value):
        self._xf = value


class First_state(State):
    def __init__(self, event_time, component: Component):
        State.__init__(self, event_time, component)

    def extern_transition(self):
        pass

    def intern_transition(self):
        self.component.transition_to(Second_state(self.component.timeBeforeStep, self.component))

    def output_method(self):
        self.component.set_outputs(self.component.myOutput, self.component.xi)
        self.component.ports[self.component.myOutput].update()

    def time_advance(self):
        pass


class Second_state(State):
    def __init__(self, event_time, component: Component):
        State.__init__(self, event_time, component)

    def intern_transition(self):
        self.component.transition_to(Third_state(math.inf, self.component))

    def output_method(self):
        self.component.set_outputs(self.component.myOutput, self.component.xf)
        self.component.ports[self.component.myOutput].update()
        pass

    def extern_transition(self):
        pass

    def time_advance(self):
        pass


class Third_state(State):
    def __init__(self, event_time, component):
        State.__init__(self, event_time, component)

    def extern_transition(self):
        pass

    def intern_transition(self):
        pass

    def output_method(self):
        pass

    def time_advance(self):
        pass
