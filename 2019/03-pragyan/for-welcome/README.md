# Challenge

> Welcome

> 50 point

> Do you think this is a normal image? No! Dig deeper to find out more.....

> file: welcome.

# Solution
問題文からして単純なステガノらしい．サクッとサクッと

### 1. binwalkでファイル抽出
```
$ binwalk welcome.jpeg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
10600         0x2968          Zip archive data, at least v2.0 to extract, uncompressed size: 9886, name: d.zip
20483         0x5003          End of Zip archive
```

抽出すると d.zipが抽出され，d.zipから，secret.bmp,とa.zipが解凍される．
a.zipないにはa.pngというファイルがパスワード付きで入っている．


### 2. パスワードを見つけてa.zipを解凍する
```
$ strings secret.bmp
okdq09i39jkc-evw.;[23760o-keqayiuhxnk42092jokdspb;gf&^IFG{:DSV>{>#Fqe'plverH%^rw[.b]w[evweA#km7687/*98<M)}?>_{":}>{>~?!@{%pb;gf&^IFG{:DSV>{>#Fqe'plverH%^rw[.b]w[evweA#km7687/*98<M)}?>_{":}>{>~?!?@{%&{:keqay^IFG{wfdoiajwlnh[8-7.=p54.b=dGhlIHBhc3N3b3JkIGlzOiBoMzExMF90aDNyMyE==
```
最後の方にbaseエンコードっぽい文字列があるのでデコードしてみる．
```
$ echo 'dGhlIHBhc3N3b3JkIGlzOiBoMzExMF90aDNyMyE==' | base64 -d
the password is: h3110_th3r3!
```
これを打ち込んでa.pngを解凍する．

### 3. a.pngの中から画像を探す．
50点なのにまだ終わらないのか・・・（困惑）

a.pngをステガノツールに突っ込んで画像解析を行う．今回は青空白猫ツールを使った．
赤色の最下位ビットを抽出して白黒画像を作ると，フラグが現れる．


# Clue
- ないです