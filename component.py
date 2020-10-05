from __future__ import annotations
from abc import ABC, abstractmethod

# List of components given to the scheduler
components = []


class Component(ABC):
    """
    Class representing a component defined by :
     - a dictionary of inputs representing the set of inputs with their names and values
     - a dictionary of outputs representing the set of inputs with their names and values
     - a dictionary of ports representing the ports connected the component with their names
     - a current state
     - the remaining time before the next event
     - the date of the last event
     - the date of the next event
     - the elapsed time in the current state
    """

    # Represents the current state of the component
    _state = None
    # Represents the list of ports indexed with their name
    _ports = {}

    def __init__(self, event_time):
        self._inputs = dict()
        self._outputs = dict()
        self._remaining_time = event_time
        self._last_event_date = 0
        self._next_event_date = 0
        self._elapsed_time = 0

        components.append(self)

    def transition_to(self, state: State):
        """
         The component allows changing the state at runtime.
        :param state: New state of the component
        :return: None
        """

        print(f"Component {type(self).__name__}: Transition to {type(state).__name__}")
        self._state = state
        self._state.component = self

    def set_initial_state(self, init_state: State) -> None:
        self._state = init_state

    def time_update_internal_transition(self, t):
        self.remaining_time = self.state.time
        self.elapsed_time = 0
        self.last_event_date = t
        self.next_event_date = t + self.state.time

    def clean_inputs(self):
        self._inputs = {}

    @property
    def ports(self):
        return self._ports

    def set_port(self, name, port: Port):
        self._ports[name] = port

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: State) -> None:
        self._state = state

    @property
    def inputs(self) -> dict:
        return self._inputs

    @inputs.setter
    def inputs(self, inputs: dict) -> None:
        self._inputs = inputs

    def set_inputs(self, key, value) -> None:
        self._inputs[key] = value

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, outputs: dict) -> None:
        self._outputs = outputs

    def set_outputs(self, key, value) -> None:
        self._outputs[key] = value

    @property
    def remaining_time(self):
        return self._remaining_time

    @remaining_time.setter
    def remaining_time(self, value):
        self._remaining_time = value

    @property
    def last_event_date(self):
        return self._last_event_date

    @last_event_date.setter
    def last_event_date(self, value):
        self._last_event_date = value

    @property
    def next_event_date(self):
        return self._next_event_date

    @next_event_date.setter
    def next_event_date(self, value):
        self._next_event_date = value

    @property
    def elapsed_time(self):
        return self._elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, value):
        self._elapsed_time = value


class State(ABC):

    @property
    def component(self):
        return self._component

    @property
    def time(self):
        return self._time

    @component.setter
    def component(self, component) -> None:
        self._component = component

    def __init__(self, state_time, component):
        self._component = component
        self._time = state_time
        # self.component.remaining_time = state_time
        self.elapsed_time = 0

    @abstractmethod
    def intern_transition(self):
        pass

    @abstractmethod
    def extern_transition(self):
        pass

    @abstractmethod
    def output_method(self):
        pass

    @abstractmethod
    def time_advance(self):
        pass


class Port(ABC):

    def __init__(self, provenance: Component, target: list, name: str):
        self._name = name
        self._from = provenance
        self._to = target

    @property
    def name(self) -> str:
        return self._name

    def update(self):
        for t in self._to:
            t.set_inputs(self._name, self._from.outputs[self._name])
        self._from.set_outputs(self._name, None)
