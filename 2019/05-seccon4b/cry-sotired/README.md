# SECCON Beginners CTF 2019 "So Tired" [warmup, Crypto]

## 問題
最強の暗号を作りました。 暗号よくわからないけどきっと大丈夫！

File: so_tired.tar.gz

## 解法
　encrypted.txtを見るとbase64でエンコードされているのでとりあえずデコードした。すると何かのファイルになっていそうだったのでファイルに出力して `file` を実行するとzlibで圧縮されていることが分かる。これをdecompressすると更に別のbase64の文字列が現れた。数回繰り返しても続いたのでPythonでスクリプトを書いた。

```python
from zlib import decompress
from base64 import b64decode

with open('encrypted.txt', 'r') as f:
    c = f.read()
    for _ in range(1000):
        m = decompress(b64decode(c.encode())).decode()
        if m.startswith('ctf4b'):
            print(m)
            break
        c = m
```

Flag: `ctf4b{very_l0ng_l0ng_BASE64_3nc0ding}`
