# InterKosenCTF writeup

## Flag Ticket [400pts, 15 solved]
### 問題
My ticket number for getting the flag is `765876346283`.
Please check if I can get the flag here.


### 解法

Cookieに `{"is_hit": false, "number": 765876346283}` をIVとAES-CBCで暗号化した結果が格納されています。暗号文は16バイトずつのブロック区切られていて、1ブロック目は`{"is_hit": false`とIVのXORを取った値を暗号化した値となっています。復号される際に再びIVとのXORが取られるので、Cookieに直接書いてあるIVを書き換えておけば、最後の'false'が'true 'へと書き換わります。

```python
from Crypto.Cipher import AES
from Crypto.Util import Padding
from binascii import hexlify, unhexlify
from ctflib import extract_flag
import requests

number = 765876346283
url = 'http://pwn.kosenctf.com:8000/check'
r = requests.post(url, data={'number':number}, allow_redirects=False)
result = unhexlify(r.cookies['result'].encode())

data = f'{{"is_hit": true , "number": {number}}}'.encode()
data = Padding.pad(data, AES.block_size)

result = list(result)
result[11] ^= ord('f')^ord('t')
result[12] ^= ord('a')^ord('r')
result[13] ^= ord('l')^ord('u')
result[14] ^= ord('s')^ord('e')
result[15] ^= ord('e')^ord(' ')
res = hexlify(bytes(result)).decode()

url = 'http://pwn.kosenctf.com:8000/result'
r = requests.post(url, cookies={'result':res})
print(extract_flag(r.text, 'KosenCTF{', '}'))

```

Flag: `KosenCTF{padding_orca1e_is_common_sense}`
