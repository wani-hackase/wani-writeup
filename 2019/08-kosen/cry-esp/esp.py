from Crypto.Util.number import *
from secret import flag, yukko
import re

assert re.match(r"^KosenCTF{.+}$", flag)

Nbits = 1024
p = getPrime(Nbits)
q = getPrime(Nbits)
n = p * q
e = 5
c = pow(bytes_to_long((yukko + flag).encode()), e, n)

print("N = {}".format(n))
print("e = {}".format(e))

print("Wow Yukko the ESPer helps you!")
print(yukko + "the length of the flag = {}".format(len(flag)))
print("c = {}".format(c))
