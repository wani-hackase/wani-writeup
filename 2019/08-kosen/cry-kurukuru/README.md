# InterKosenCTF writeup
## Kurukuru Shuffle [200pts, 53 solved]
### 問題
Please! My...



### 解法

与えられたファイルを見てみると、Flagは3つの乱数をパラメーターとしてシャッフルされているのが分かります。パラメーターとして使われている変数の取りうる範囲はFlagの長さ $L$ にほぼ等しく、$L=53$ と小さいので$O(L^4)$で全探索しました。

```python
f = open('encrypted')
enc = f.read().strip()
f.close()
L = len(enc)

for k in range(1, L):
    for a in range(L):
        for b in range(L):
            if a == b:
                continue
            flag = list(enc)
            i = k
            for _ in range(L):
                s = (i+a)%L
                t = (i+b)%L
                flag[s], flag[t] = flag[t], flag[s]
                i = (i+k)%L
            flag = ''.join(flag)
            if flag.startswith('KosenCTF{'):
                print(flag)
                break
```

Flag: `KosenCTF{us4m1m1_m4sk_s3np41_1s_r34lly_cut3_38769915}`
