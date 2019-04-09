from Crypto.Util.number import *
from math import gcd

n = 379557705825593928168388035830440307401877224401739990998883
e = 65537
c = 29031324384546867512310480993891916222287719490566042302485

p = 564819669946735512444543556507
q = 671998030559713968361666935769


def lcm(x, y):
    return (x * y) // gcd(x, y)


def ex_euclid(x, y):
    c0, c1 = x, y
    a0, a1 = 1, 0
    b0, b1 = 0, 1

    while c1 != 0:
        m = c0 % c1
        q = c0 // c1

        c0, c1 = c1, m
        a0, a1 = a1, (a0 - q * a1)
        b0, b1 = b1, (b0 - q * b1)

    return a0, b0


t = lcm(p - 1, q - 1)
a, b = ex_euclid(e, t)
d = a % t

m = pow(c, d, n)

print(long_to_bytes(m))
