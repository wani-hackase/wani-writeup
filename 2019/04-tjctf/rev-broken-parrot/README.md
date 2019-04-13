# TJCTF 2019 "Broken Parrot"

## Description

I found this annoying [parrot](). I wish I could just ignore it, but I've heard that it knows something special.

## Solution

parrotという名前の32bit ELF実行ファイルが与えられる。
とりあえずstringsコマンドを使ってみるとflagらしきものがあった。
```
$ strings parrot
/lib/ld-linux.so.2
libc.so.6
_IO_stdin_used
puts
stdin
printf
fgets
strlen
__libc_start_main
__gmon_start__
GLIBC_2.0
PTRh
UWVS
t$,U
[^_]
Say something to the parrot:
You got my flag!
a %s
;*2$"
tjctf{my_b3l0v3d_5qu4wk3r_w0n7_y0u_l34v3_m3_4l0n3}
GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.11) 5.4.0 20160609
crtstuff.c
__JCR_LIST__
```

`tjctf{my_b3l0v3d_5qu4wk3r_w0n7_y0u_l34v3_m3_4l0n3}``をsubmitして終わりかと思いきやそうではなかった。

parrotを実行してみると下の画像のように入力したものをそのままオウム返しするものだとわかる。


```
$ ./parrot
Say something to the parrot: AAAAAAAA
AAAAAAAA
Say something to the parrot: BBBB
BBBB
Say something to the parrot: ABCDE
ABCDE
Say something to the parrot:

```

次にGDBを使ってこのプログラムが何を行っているのかを調べる。

入力の際にfgetsが使われていたのでその直前にブレークポイントを仕掛けておき、そこからステップ実行を行いながらレジスタの値を監視する。
