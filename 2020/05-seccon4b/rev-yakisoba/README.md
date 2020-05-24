# SECCON Beginners CTF 2020 "yakisoba" writeup

## 問題

```
Would you like to have a yakisoba code?

(Hint: You'd better automate your analysis)
```

## 解法

フラグを入力するように言われて、正しいフラグかどうか判定する実行ファイル

angr で判定条件を満たす入力を探してもらう

```python
import angr

project = angr.Project('./yakisoba')
entry = project.factory.entry_state()
simgr = project.factory.simgr(entry)
simgr.explore()

states = simgr.deadended
for state in states:
    flag = b"".join(state.posix.stdin.concretize())
    print(flag)
```

```
ctf4b{sp4gh3tt1_r1pp3r1n0}
```
