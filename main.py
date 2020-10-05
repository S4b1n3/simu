from generator import Generator
from buffer import Buffer
from processor import Processor
from scheduler import Scheduler
import component
import math

if __name__ == "__main__":
    print("------------------------------\n")
    print("t = 0")
    compo_generator = Generator(2)
    compo_buffer = Buffer(math.inf)
    compo_processor = Processor(math.inf)

    port_gen_buf = component.Port(compo_generator, [compo_buffer], "job")
    port_proc_buf = component.Port(compo_processor, [compo_buffer], "done")
    port_buf_proc = component.Port(compo_buffer, [compo_processor], "req")

    compo_buffer.set_port(port_buf_proc.name, port_buf_proc)
    compo_buffer.set_port(port_gen_buf.name, port_gen_buf)
    compo_buffer.set_port(port_proc_buf.name, port_proc_buf)

    compo_generator.set_port(port_gen_buf.name, port_gen_buf)

    compo_processor.set_port(port_buf_proc.name, port_buf_proc)
    compo_processor.set_port(port_proc_buf.name, port_proc_buf)

    print(component.components)

    launch_test = Scheduler(component.components, 6)

    launch_test.exec()
