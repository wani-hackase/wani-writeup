# 問題 Pwn 零は？
```bash
$ nc zerois-o-reiwa.seccon.jp 23615
[1/100]
0=2-?
?=2
[2/100]
0=?+17-48
?=31
[3/100]
0=13-?+38+9
?=
```

### 解説
- 上記の問題に記述してる通り指定されたサーバーにncすると、数式が与えられるので、適切な計算結果を送信しなければならない。

- この問題のポイントは２点あって、サーバーからの出力を元に計算をして、その結果をサーバーに送信することである。

- サーバーとのやり取りには以下の `pwntools` を使い、計算には `sympy` を使う。

- サーバーからの出力を計算するに当たって、最初は `eval()` を使って ? を全探索していたが、計算量が膨大になるので、sympy の solve() を使って、方程式を解くことにした。

- 別ファイルのsolve.pyを実行すると、`SECCON{REIWA_is_not_ZERO_IS}`が得られる。

### 参考
- [pwntools](https://github.com/arthaud/python3-pwntools)
- [sympy](https://www.sympy.org/en/index.html)
