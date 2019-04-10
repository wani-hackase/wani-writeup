# VolgaCTF 2019 Qualifier "Blind" writeup

## Description

Please teach me how to be a comprehension master, all my friends are counting on me!

[comprehensive.py](comprehensive.py)

Original output: 225, 228, 219, 223, 220, 231, 205, 217, 224, 231, 228, 210, 208, 227, 220, 234, 236, 222, 232, 235, 227, 217, 223, 234, 2613

Note: m and k were 24 and 8 characters long originally and english characters.

## Solution

comprehensive.pyを見る。

```python

m = 'tjctf{?????????????????}'.lower()
k = '????????'.lower()

f = [[ord(k[a]) ^ ord(m[a+b]) for a in range(len(k))] for b in range(0, len(m), len(k))]
g = [a for b in f for a in b]
h = [[g[a] for a in range(b, len(g), len(f[0]))] for b in range(len(f[0]))]
i = [[h[b][a] ^ ord(k[a]) for a in range(len(h[0]))] for b in range(len(h))]
print(str([a + ord(k[0]) for b in i for a in b])[1:-1] + ',', sum([ord(a) for a in m]))

```

f, g, h, iがワンライナーで、len(hoge)が複雑なので書き換えてみる。

```python

f = []
g = []
h = []
i = []

# f
for b in range(0, 24, 8):
	for a in range(8):
		f.append(ord([k[a]) ^ ord(m[a+b])])

# g
for b in f:
	for a in b:
		g.append(a)

# h
for b in range(8):
	tmp = []
	for a in range(b, 24, 8):
		tmp.append(g[a])
	h.append(tmp)

# i
for b in range(8):
	tmp = []
	for a in range(3):
		tmp.append(h[b][a] ^ ord(k[a]))
	i.append(tmp)
```

以上から、0≦j≦39として、
i[j] = m[(j%3)*8 + j//3] ^ k[j//3] ^ k[j%3]
となる。

添字が複雑だが、各配列毎にprintで表示すると関係がわかりやすい。

また、最後に表示している配列を s とすると
`s[j] = m[(j%3)*8 + j//3] ^ k[j//3] ^ k[j%3] + k[0]`
となる。

ここでs[0]を考えると、
`s[0] = m[0] ^ k[0] ^ k[0] + k[0]`
XORの性質から変形できて、
`k[0] = s[0] - m[0]`
`k[0] = 109`

`k[0]`が分かったので、`m[0], ... ,m[5], m[23]` を利用して順次計算できて、`k[6]`以外全て分かる。

`k[6]`は総当たりで求めることができて、ciphertextの末尾の値が復号後の`ord(m[j])`の総和であることから、とから
これが一致した時復号した値がフラグとなっている。


Flag: `tjctf{oooowakarimashita}`

おおおお分かりました！
