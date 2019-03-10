# Challenge

> Magic PNGs 

> 100 point

> Magic PNGs:

> Can you help me open this zip file? I seem to have forgotten its password. I think the image file has something to do with it.

> file: tryme.zip you_cant_see_me.png


# Solution
問題文にもあるように，tryme.zipには鍵がかかっており，パスワードを求められる．
いろいろパスワードクラックを試すが効果なし．．．おとなしくPNGを弄ってパスワードを探すことにする．


### 1. ．pngのマジックナンバーを修正する ＆ exiftoolを使う
まずは画像系Forensicsのお約束，strings, binwalk, exiftool, foremost, stegdetectとかを行う．
．．．が反応はなく，exiftoolでも情報が見れない．問題文からマジックナンバー辺りが壊れていると思い，バイナリエディタを起動する．

```
$ exiftool you_cant_see_me.png
ExifTool Version Number         : 10.80
File Name                       : you_cant_see_me.png
Directory                       : .
File Size                       : 6.0 kB
File Modification Date/Time     : 2019:03:09 00:27:39+09:00
File Access Date/Time           : 2019:03:09 00:27:16+09:00
File Inode Change Date/Time     : 2019:03:09 00:41:17+09:00
File Permissions                : rwxrwxrwx
Error                           : File format error
```

案の定，最初の8バイトが`89 50 4E 47 2E 0A 2E 0A`となっていたのでPNGのフォーマット(https://www.setsuki.com/hsp/ext/png.htm) にしたがって
`89 50 4E 47 0D 0A 1A 0A`に書き換える．その後exiftoolを使うとexif情報がみられる．

```
$ exiftool mod_you_cant_see_me.png
ExifTool Version Number         : 10.80
File Name                       : mod_you_cant_see_me.png
Directory                       : .
File Size                       : 6.0 kB
File Modification Date/Time     : 2019:03:09 00:41:06+09:00
File Access Date/Time           : 2019:03:09 00:41:06+09:00
File Inode Change Date/Time     : 2019:03:09 00:41:06+09:00
File Permissions                : rwxrwxrwx
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 205
Image Height                    : 246
Bit Depth                       : 8
Color Type                      : Palette
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Gamma                           : 2.2
White Point X                   : 0.3127
White Point Y                   : 0.329
Red X                           : 0.64
Red Y                           : 0.33
Green X                         : 0.3
Green Y                         : 0.6
Blue X                          : 0.15
Blue Y                          : 0.06
Palette                         : (Binary data 132 bytes, use -b option to extract)
Background Color                : 0
Pixels Per Unit X               : 2835
Pixels Per Unit Y               : 2835
Pixel Units                     : meters
Datecreate                      : 2018-00-00T12:52:25+00:00
Datemodify                      : 2018-00-00T12:53:20+00:00
Artist                          : md5_MEf89jf4h9
Image Size                      : 205x246
Megapixels                      : 0.050
```

Artist情報に怪しい文字列 md5_MEf89jf4h9 がある．
これをzipに打ち込むがNG．md5でエンコードしたり，加工するがNG．
ここで一度画像を見てみようとするが，まだエラーでみることができない．どうやらもう一山あるようだ・



### 2. IDATを修正して画像を見れるようにする
もう一度バイナリエディタで画像を開いてみると，IDATがないことに気づく．そこでヘッダ部を読んで行くと，小文字でidatと書かれている部分を発見する．
これを大文字のIDATに書き換えると画像が見れるようになる．




### 3. 画像内にかかれているコードをmd5でエンコードしてzipを開く  → Flagゲット
画像を開くと，中にはh4CK3Manという文字列が！ やったぜ！とzipに打ち込むがパスワードエラー．
ここで先程のmd5_MEf89jf4h9に気づく，もしやmd5でエンコードではと思い，エンコードしたパスを打ち込むーとビンゴ！
flag.txtを見れる．


# Clue
- 問題名からマジックナンバー関連かな．．．と推測できる
- IDATエラーを検知するにはpngcheckを使うのもよい．今回はすぐにみつかったから良いが．．