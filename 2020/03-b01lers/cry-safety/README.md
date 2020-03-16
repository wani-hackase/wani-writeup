# b01lers CTF  Safety In Numbers [Crypto]

## Solution
公開鍵がPEM形式のファイルで与えられる。値を確認するために読み込もうとするとNが非常に大きいために処理が終わらない。ただし e が 0x10001(=65537) であることは分かる。
Nが非常に大きいので単純にe乗根を取ることを試してみる。gmpy2.iroot()を用いると丁度e乗根になっているかを同時に調べられる。実際、e乗根は元のFlagとなっていた。

```python
import gmpy2

e = 0x10001

with open('flag.enc', 'rb') as f:
    flag = f.read()

flag = int.from_bytes(flag, byteorder='little')
m, exact = gmpy2.iroot(flag, e)
m = int(m)

if exact:
    flag = m.to_bytes(m.bit_length()//8+1, byteorder='little')
    print(flag)
else:
    print('Failed')
```

Flag: `pctf{!fUtuR3_pR00f}`
