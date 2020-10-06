from abc import ABC
import matplotlib.pyplot as plt


class Scheduler(ABC):

    def __init__(self, components, end_time):
        self._global_time_advancement = 0
        self._end_time = end_time
        self._min_remaining_time = None
        self._component_set = components

    def exec(self):
        points_x = []
        points_y = []
        points_y_Int = []
        iter = 0
        while self._global_time_advancement <= self._end_time:
            iter = iter + 1
            set_remaining_time = []
            imminent_components = []

            '''
            for c in self._component_set:
                c.clean_inputs()'''

            for c in self._component_set:
                if type(c).__name__ == "Adder":
                    points_x.append(self._global_time_advancement)
                    #points_y.append(c.outputs["sum"])
                    points_y.append(c.currentSum)
                if type(c).__name__ == "Integrator":
                    points_y_Int.append(c.x)
                    print("Integrator inputs : ",c.inputs)
                set_remaining_time.append(c.remaining_time)
            print(set_remaining_time)
            self._min_remaining_time = min(set_remaining_time)
            for c in self._component_set:
                if c.remaining_time == self._min_remaining_time:
                    imminent_components.append(c)
            #for i in imminent_components:
                #print("\nImminent components")
                #print(f"Component {type(i).__name__}")
                #print("Time remaining : " + str(i.remaining_time))
            self._global_time_advancement += self._min_remaining_time
            print("------------------------------\n")
            print("t = " + str(self._global_time_advancement))
            for c in self._component_set:
                c.remaining_time -= self._min_remaining_time
                c.state.elapsed_time += self._min_remaining_time
            for c in imminent_components:
                c.state.output_method()
            for c in self._component_set:
                input_empty = True
                for v in c.inputs.values():
                    if v is not None:
                        input_empty = False
                if c in imminent_components and input_empty:
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
                    print(f"Component {type(c).__name__} : conflict")
                    c.state.conflict()
                    #c.state.extern_transition()
                    #c.state.intern_transition()
                    '''
                        Update tr, e, tl, tn of c component
                    '''
                    c.time_update_internal_transition(self._global_time_advancement)
            if iter > 4:
                #break
                pass

        plt.plot(points_x, points_y)
        plt.plot(points_x, points_y_Int)
        plt.show()
