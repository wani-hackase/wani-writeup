from ctflib import *
from pwn import *

io = remote('pwn.kosenctf.com', '8002')

io.recvline() # I encrypted my secret!!!
c = int(io.recvline())
io.recvline() # I encrypt your message ;)

pt1 = int('1'+'0'*382, 2)
io.sendline(str(pt1))
io.recvline()
c1 = int(io.recvline())

pt2 = pt1+1
io.sendline(str(pt2))
io.recvline()
c2 = int(io.recvline())

n = (c2-c1)
n %= n*n

assert(pow(1+n, pt1, n*n) == c1)
assert(pow(1+n, pt2, n*n) == c2)

print(n)
key = (c-1)//n
print(its(key))

io.interactive()
