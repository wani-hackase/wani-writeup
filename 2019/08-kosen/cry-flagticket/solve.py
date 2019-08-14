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
