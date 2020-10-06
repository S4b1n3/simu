from component import Component, State
import math


class Adder(Component):
    def __init__(self, s0_time):
        Component.__init__(self, math.inf)
        self._inputs["01"] = None
        self._inputs["02"] = None
        self._inputs["03"] = None
        self._inputs["04"] = None
        self._outputs["sum"] = None
        self._currentSum = 0
        self.set_initial_state(Get(math.inf, self))

    @property
    def currentSum(self):
        return self._currentSum

    @currentSum.setter
    def currentSum(self, value):
        self._currentSum = value

    def clean_inputs(self):
        self._inputs["01"] = None
        self._inputs["02"] = None
        self._inputs["03"] = None
        self._inputs["04"] = None


class Get(State):
    def __init__(self, event_time, component: Component):
        State.__init__(self, event_time, component)
        print(f"Component : {type(self).__name__}")

    def extern_transition(self):
        if self.component.inputs["01"] or self.component.inputs["02"] or self.component.inputs["03"] or self.component.inputs["04"] is not None:
            print(self.component.inputs)
            self.component.transition_to(Send(0, self.component))

    def intern_transition(self):
        pass

    def output_method(self):
        pass

    def time_advance(self):
        pass


class Send(State):
    def __init__(self, event_time, component: Component):
        State.__init__(self, event_time, component)
        print(f"State send : {type(self).__name__}")

    def intern_transition(self):
        self.component.transition_to(Get(math.inf, self.component))

    def output_method(self):
        self.component.currentSum = 0
        print(self.component.inputs)
        if self.component.inputs["01"] is not None:
            self.component.currentSum = self.component.currentSum + self.component.inputs["01"]
        if self.component.inputs["02"] is not None:
            self.component.currentSum = self.component.currentSum + self.component.inputs["02"]
        if self.component.inputs["03"] is not None:
            self.component.currentSum = self.component.currentSum + self.component.inputs["03"]
        if self.component.inputs["04"] is not None:
            self.component.currentSum = self.component.currentSum + self.component.inputs["04"]

        self.component.set_outputs("sum", self.component.currentSum)
        print(self.component.outputs)
        self.component.ports["sum"].update()

    def extern_transition(self):
        pass

    def time_advance(self):
        pass

    def conflict(self):
        self.intern_transition()
