# Ksnctf 28 Lo-Tech Cipher

<http://ksnctf.sweetduet.info/q/28/secret.zip>

unzip で ２つの png

ステガノグラフィー系と思い, とりあえず png を exiftool と binwalk → 特に何もなし

２つの png を重ねると The last share is hidden in the zip と言われる

```
$ exiftool secret.zip

ExifTool Version Number         : 11.11
File Name                       : secret.zip
Directory                       : .
File Size                       : 276 kB
File Modification Date/Time     : 2019:01:17 22:34:16+09:00
File Access Date/Time           : 2019:01:17 22:34:16+09:00
File Inode Change Date/Time     : 2019:01:17 22:34:16+09:00
File Permissions                : rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 640
Image Height                    : 480
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Warning                         : [minor] Trailer data after PNG IEND chunk
Image Size                      : 640x480
Megapixels                      : 0.307
```

```
$ binwalk secret.zip

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 640 x 480, 8-bit/color RGBA, non-interlaced
41            0x29            Zlib compressed data, default compression
95256         0x17418         Zip archive data, at least v2.0 to extract, compressed size: 93428, uncompressed size: 94601, name: share1.png
188724        0x2E134         Zip archive data, at least v2.0 to extract, compressed size: 93663, uncompressed size: 94902, name: share2.png
282539        0x44FAB         End of Zip archive
```

ヘッダー情報が PNG である

よって拡張子を zip から png にして先程の二枚の画像に重ねると

```
FLAG_XXXXXXXXXXXXXXXX
Congratulations!
If you have interested is this type of cryptgraphy, google "Visual cryptography".
```

flag get
