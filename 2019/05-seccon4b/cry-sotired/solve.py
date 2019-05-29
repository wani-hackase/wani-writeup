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
