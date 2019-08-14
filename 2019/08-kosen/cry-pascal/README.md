# InterKosenCTF writeup

## pascal homomorphicity [333pts, 20 solved]

### 問題
nc pwn.kosenctf.com 8002


### 解法
nc して最初に与えられる数字 c は、`c ≡ (1+n)^ Flag mod n^2` であり、以降こちらからFlagのbit長以上の整数 x を送ってやると、`y = (1+n)^x mod n^2` が返ってきます。Paillier暗号ですね。
ここで $(1+n)^x$ を二項定理で展開すると、
`(1+n)^x ≡ 1+nx mod n^2`
であることが分かります。
これを利用して、Flagのbit長以上の適当な2つの整数 `x1 = X, x2 = X+1` を送ると、それぞれ `y1, y2` が返ってきて
`y2-y1 ≡ (1+nX+n)-(1+nX) ≡ n mod n^2`
となって、n が得られます。

求めた n を利用すると `c ≡ 1+nFlag mod n^2` であるから、
`Flag ≡ (c-1)/n mod n^2`
というように計算が可能です。

Flag: `KosenCTF{Th15_15_t00_we4k_p41ll1er_crypt05y5tem}`
