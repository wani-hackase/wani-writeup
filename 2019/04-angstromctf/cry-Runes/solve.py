import binascii
import math

from Crypto.Util.number import inverse

n = 99157116611790833573985267443453374677300242114595736901854871276546481648883
g = 99157116611790833573985267443453374677300242114595736901854871276546481648884
c = 2433283484328067719826123652791700922735828879195114568755579061061723786565164234075183183699826399799223318790711772573290060335232568738641793425546869
p = 310013024566643256138761337388255591613
q = 319848228152346890121384041219876391791


def L(u):
    return (u - 1) // n


def lcm(x, y):
    return (x * y) // math.gcd(x, y)


if __name__ == '__main__':
    lam = lcm(p-1, q-1)
    mu = inverse(L(pow(g, lam, n ** 2)), n)
    ans = L(pow(c, lam, n ** 2)) * mu % n

    print(binascii.unhexlify(hex(ans)[2:]))