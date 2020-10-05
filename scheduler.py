from abc import ABC


class Scheduler(ABC):

    def __init__(self, components, end_time):
        self._global_time_advancement = 0
        self._end_time = end_time
        self._min_remaining_time = None
        self._component_set = components

    def exec(self):
        set_remaining_time = []
        imminent_components = []
        while self._global_time_advancement <= self._end_time:
            for c in self._component_set:
                set_remaining_time.append(c.remaining_time)
            self._min_remaining_time = min(set_remaining_time)
            for c in self._component_set:
                if c.remaining_time == self._min_remaining_time:
                    imminent_components.append(c)
            for i in imminent_components:
                print(f"Component {type(i).__name__}")
                print("Time remaining : " + str(i.remaining_time))
            self._global_time_advancement += self._min_remaining_time
            print("------------------------------\n")
            print("t = " + str(self._global_time_advancement))
            for c in self._component_set:
                c.remaining_time -= self._min_remaining_time
                c.state.elapsed_time += self._min_remaining_time
            for c in imminent_components:
                c.state.output_method()
            for c in self._component_set:
                input_empty = False
                for v in c.inputs.values():
                    if v is None:
                        input_empty = False
                if c in imminent_components and (input_empty and len(c.inputs) != 0):
                    print(f"Component {type(c).__name__} : internal transition")
                    c.state.intern_transition()
                    c.time_update_internal_transition(self._global_time_advancement)

                elif c not in imminent_components and not input_empty:
                    print(f"Component {type(c).__name__} : external transition")
                    c.state.extern_transition()
                    c.time_update_internal_transition(self._global_time_advancement)
                    '''
                        Update tr, e, tl, tn of c component
                    '''
                    c.time_update_internal_transition(self._global_time_advancement)
                    
                elif c in imminent_components and not input_empty:
                    # c.conflict()
                    c.state.extern_transition()
                    '''
                        Update tr, e, tl, tn of c component
                    '''
                    c.time_update_internal_transition(self._global_time_advancement)

            for c in self._component_set:
                c.clean_inputs()
