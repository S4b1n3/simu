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
            print("t = " + str(self._global_time_advancement))
            for c in self._component_set:
                set_remaining_time.append(c.remaining_time)
            self._min_remaining_time = self._component_set[min(set_remaining_time)].remaining_time
            for c in self._component_set:
                if c.remaining_time == self._min_remaining_time:
                    imminent_components.append(c)
            self._global_time_advancement += self._min_remaining_time
            for c in self._component_set:
                c.remaining_time -= self._min_remaining_time
                c.state.elapsed_time += self._min_remaining_time
            for c in imminent_components:
                c.state.output_method()
            for c in self._component_set:
                if c in imminent_components and not c.inputs:
                    c.state.intern_transition()
                    c.time_update_internal_transition(self._global_time_advancement)

                elif c not in imminent_components and c.inputs:
                    c.state.extern_transition()
                    c.time_update_internal_transition(self._global_time_advancement)
                    '''
                        Update tr, e, tl, tn of c component
                    '''
                    c.time_update_internal_transition(self._global_time_advancement)
                    
                elif c in imminent_components and c.inputs:
                    # c.conflict()
                    c.state.extern_transition()
                    '''
                        Update tr, e, tl, tn of c component
                    '''
                    c.time_update_internal_transition(self._global_time_advancement)

            for c in self._component_set:
                c.clean_inputs()
