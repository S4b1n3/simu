from integrateur_discret import Integrator
from Event_integrator import EventIntegrator
from step import Step
from adder import Adder
from scheduler import Scheduler
import component
import math

if __name__ == "__main__":
    print("------------------------------\n")
    print("t = 0")

    step1 = Step(0.65, 1, -3, "01")
    step2 = Step(0.35, 0, 1, "02")
    step3 = Step(1, 0, 1, "03")
    step4 = Step(1.5, 0, 4, "04")

    adder = Adder(math.inf)

    print(component.components)

    port1 = component.Port(step1, [adder], "01")
    port2 = component.Port(step2, [adder], "02")
    port3 = component.Port(step3, [adder], "03")
    port4 = component.Port(step4, [adder], "04")

    step1.set_port(port1.name, port1)
    step2.set_port(port2.name, port2)
    step3.set_port(port3.name, port3)
    step4.set_port(port4.name, port4)

    adder.set_port(port1.name, port1)
    adder.set_port(port4.name, port4)
    adder.set_port(port3.name, port3)
    adder.set_port(port2.name, port2)


    '''
            ____________________________________________________________
            il faut choisir ici quel integrateur utiliser et
            par consequent commenter l'autre
            ____________________________________________________________
    '''

    
    integrator = Integrator(10**(-4))
    port_inte_out = component.Port(integrator, [], "sx")
    port_sum = component.Port(adder, [integrator], "sum")
    integrator.set_port(port_sum.name, port_sum)
    integrator.set_port(port_inte_out.name, port_inte_out)


    '''
    integratorEvent = EventIntegrator(math.inf)
    port_inteEvent_out = component.Port(integratorEvent, [], "sq")
    port_sum = component.Port(adder, [integratorEvent], "sum")
    integratorEvent.set_port(port_sum.name, port_sum)
    integratorEvent.set_port(port_inteEvent_out.name, port_inteEvent_out)
    '''

    adder.set_port(port_sum.name, port_sum)

    launch_test = Scheduler(component.components, 2)

    launch_test.exec()



