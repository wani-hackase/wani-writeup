import ctypes
import hashlib
import struct
import socket
import sys



class timeval(ctypes.Structure):
    _fields_ = \
    [
      ("tv_sec", ctypes.c_long),
      ("tv_usec", ctypes.c_long)
    ]



def bruteforce(md5msg):
    print("bruteforce")
    tv = timeval()

    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    libc.gettimeofday(ctypes.byref(tv), None)
    start_t = (tv.tv_sec - 2) * 1000000
    end_t = start_t + 2 * 1000000

    for i in range(end_t - start_t):
        t = start_t + i

        libc.srand(t)
        r = libc.rand()
        r = libc.rand()
        r = libc.rand()
        md5 = hashlib.md5()
        md5.update(struct.pack("<I", r))
        s = md5uuid(md5.hexdigest())
        if s == md5msg:
            print("t = " + str(t))
            exit(1)



def md5uuid(str):
    return str[14] + str[15] + str[12] + str[13] + str[10] + str[11] + str[8] + str[9] + str[6] + str[7] + str[4] + str[5] + str[2] + str[3] + str[0] + str[1] + str[16 + 14] + str[16 + 15] + str[16 + 12] + str[16 + 13] + str[16 + 10] + str[16 + 11] + str[16 + 8] + str[16 + 9] + str[16 + 6] + str[16 + 7] + str[16 + 4] + str[16 + 5] + str[16 + 2] + str[16 + 3] + str[16 + 0] + str[16 + 1]



def read_until(sock, s):
    line = b""
    while line.find(s) < 0:
        line += sock.recv(1)
    return line

host = "secureshell.wpictf.xyz"
port = 31339

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
print(host)
print(port)
sock.connect((host, port))

ret = read_until(sock, b"Enter the password")
sock.sendall(b"aaaa\n")

ret = read_until(sock, b"attempt #2")
print(ret)
md5msg = ret[89:89+32].decode("utf-8")

bruteforce(md5msg)
print("not solved")

