import ctypes
import hashlib
import struct

libc = ctypes.cdll.LoadLibrary("libc.so.6")
t = 0x75ad0c3b
libc.srand(t)

r = libc.rand()
print("%x" % (r))
md5 = hashlib.md5(struct.pack(">I", r))
print(md5.hexdigest())

r = libc.rand()
print("%x" % (r))
md5 = hashlib.md5(struct.pack(">I", r))
print(md5.hexdigest())

r = libc.rand()
print("%x" % (r))
md5 = hashlib.md5(struct.pack(">I", r))
print(md5.hexdigest())

r = libc.rand()
print("%x" % (r))
md5 = hashlib.md5(struct.pack(">I", r))
print(md5.hexdigest())

