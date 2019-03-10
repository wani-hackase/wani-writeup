# Pragyan CTF 2019 "EXORcism" writeup

## Description

My friend Alex needs your help very fast. He has been possessed by a ghost and the only way to save him is if you tell the flag to the ghost. Hurry up, time is running out!

## Solution

とりあえずテキストファイルの全体を見たいが、一文字ごとに改行されているのが厄介なので `tr -d '\r\n' `で取り払う。その結果を出力してエディタで開くと、0 がある決まった範囲に現れる事が分かる。

![a](a.png "a")

現れたパターンを観察していると、QRコードっぽいことが分かる。文字数を調べるとちょうど10,000文字であったので、とりあえず100文字ずつで改行した。

すると、このようになった。

![b](b.png "b.png")

確かにQRコードになっていることが分かる。
これを画像に変換して読み取る。

![qr](qr.png "qr")

読み取った結果は
`160f15011d1b095339595138535f135613595e1a`

16進数→文字列の変換をするが、`9YQ8S_VY^` となり、ただ変換するだけでは意味のある文字列は得られなかった。
ここで、問題名 EXORcism をヒントにXORを取るのだろうと予想したが、何とのXORを取ればよいかが分からない。復号結果は Flag になっているだろうと予想し、読み取った結果を文字列に直したときの先頭5文字と`pctf{`の5文字で試しにXORを取ってみた。すると`flagf`という文字列が得られた。`flagflagflagfl...`と続くと予想し、これとQRコードの復号結果のXORを取ると Flag が取れた。

```python
from PIL import Image
from pyzbar.pyzbar import decode

def xor_strings(s, t):
    if isinstance(s, str):
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))
    else:
        return bytes([a ^ b for a, b in zip(s, t)])

image = Image.open('qr.png')
ans = ''
d = decode(image)[0][0].decode()
for a, b in zip(d[::2], d[1::2]):
    ans += chr(int(a+b, 16))

ans = ''.join(ans)
print(d)
print(ans)
print(xor_strings(ans, 'flagflagflagflagflagflagflagflag'))

```



Flag : `pctf{wh4_50_53r1u5?}`

