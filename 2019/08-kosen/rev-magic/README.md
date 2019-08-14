# InterKosenCTF "magic function" writeup

## Challenge

```
Rumor has it that three simple functions may generate the flag.
```

## Solution

[SECCON Beginners CTF 2019 "Leakage" writeup](https://github.com/wani-hackase/wani-writeup/tree/master/2019/05-seccon4b/rev-leakage)

と同手法で angr で解きました。本来ならきちんとソルバを書かないといけないのですが・・・

```python
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
```

[運営解法](https://hackmd.io/@theoldmoon0602/B15VFsylB)
