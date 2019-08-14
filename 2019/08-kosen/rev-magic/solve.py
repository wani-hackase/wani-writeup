import angr
import claripy

project = angr.Project("./chall")
argv1 = claripy.BVS("argv1", 100 * 8)
initial_state = project.factory.entry_state(args=["./chall", argv1])

sm = project.factory.simulation_manager(initial_state)
sm.explore(find=0x40086a)

f = sm.found[0]
solution = f.solver.eval(argv1, cast_to=bytes)
print(repr(solution))

# KosenCTF{fl4ggy_p0lyn0m}
