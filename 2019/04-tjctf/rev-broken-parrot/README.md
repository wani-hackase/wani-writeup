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

`tjctf{my_b3l0v3d_5qu4wk3r_w0n7_y0u_l34v3_m3_4l0n3}`をsubmitして終わりかと思いきやそうではなかった。

parrotを実行してみると下の画像のように入力したものをそのままオウム返しするものだとわかる。
おそらく正しいフラグを入力すると`You got my flag!`が表示されそう。


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

`strlen`関数の直後に`cmp eax 0x22`という命令があったので入力された文字数が34文字（改行コードを含めて）であることを調べていた。
比較した結果、文字数が一致しない場合には`jne`でオウム返しのコード部分へと飛ばされている。
つまり、FLAGの文字数は33文字ということがわかった。

入力の際にfgetsが使われていたのでその直前にブレークポイントを仕掛けておき、そこからステップ実行を行いながらレジスタの値を監視する。

ステップ実行しながらeaxとedxの値を注意して見ていると、eaxには`t, j, c, t, f, ...`という文字があらわれた。また、edxには入力した文字が
１文字ずつあらわれた。`cmp al, dl`によって文字列の先頭から一文字づつ比較され、すべて一致していた場合に`You got my flag!`が出力されるようになっていたので、
eaxに現れる文字を見ていけばそれがFLAGのはず。

と、思いきや少しだけ違った。

入力した文字列が先頭から順番に比較されているものかと思っていたが、実は`{}の中の４個目の文字だけ比較されていなかった`。
これは、入力文字列に`tjctf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}`と入れるとどの文字が比較されているのかがわかるので、確認しやすかった。

`tjctf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}`の例では、`D`の文字がedxにあらわれなかった。


わからなかったのでとりあえずステップ実行でその後のプログラムへと進んでみる。

すると、eaxのところに`D`の文字が出てきてその直後に

```
0x80485d9 <main+270>:	cmp    al,0x64
0x80485db <main+272>:	je     0x80485e4 <main+281>
```

とあったのでここで４文字目が比較されていることがわかった。

ASCIIコードで0x64は`d`であるのでこれを４文字目にいれてFLAGゲット

```
$ ./parrot
Say something to the parrot: tjctf{3d_d0n7_y0u_l34v3_m3_4l0n3}
You got my flag!
```


