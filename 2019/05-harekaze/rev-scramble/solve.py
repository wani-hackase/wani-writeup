import angr

proj = angr.Project("./scramble")

# puts("Correct!") のアドレス
target_addr = 0x40073E

state = proj.factory.entry_state()
simgr = proj.factory.simgr(state)
simgr.explore(find=target_addr)
state = simgr.found[0]
print(state.posix.dumps(0))
