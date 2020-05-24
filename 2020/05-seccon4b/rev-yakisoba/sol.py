import angr

project = angr.Project('./yakisoba')
entry = project.factory.entry_state()
simgr = project.factory.simgr(entry)
simgr.explore()

states = simgr.deadended
for state in states:
    flag = b"".join(state.posix.stdin.concretize())
    print(flag)
