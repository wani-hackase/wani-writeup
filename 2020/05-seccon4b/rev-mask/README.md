# SECCON Beginners CTF 2020 "mask" writeup

## 問題

```
The price of mask goes down. So does the point (it's easy)!

(SHA-1 hash: c9da034834b7b699a7897d408bcb951252ff8f56)
```

## 解法

コマンドライン引数にフラグを入れて実行して正しいフラグか判定する実行ファイル

angr で 0x4012d6 に到達するための入力を計算してもらう

```python
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
```

```
ctf4b{dont_reverse_face_mask}
```
