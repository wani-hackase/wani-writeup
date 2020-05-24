import angr
import claripy

project = angr.Project("./mask")
argv1 = claripy.BVS("argv1",100*8)
initial_state = project.factory.entry_state(args=["./mask",argv1])
sm = project.factory.simulation_manager(initial_state)
sm.explore(find=0x4012d6)
found = sm.found[0]
solution = found.solver.eval(argv1, cast_to=bytes)
print(repr(solution))
