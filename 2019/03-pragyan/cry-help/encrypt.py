from Crypto.Util.number import *
import random

def nextPrime(prim):
    if isPrime(prim):
        return prim
    else:
        return nextPrime(prim+1)

p = getPrime(512)
q = nextPrime(p+1)
while p%4 != 3 or q%4 !=3:
    p = getPrime(512)
    q = nextPrime(p+1)

n = p*q
m = open('secret.txt').read()
m = bytes_to_long(m)

m = m**e
c = (m*m)%n
c = long_to_bytes(c)
c = c.encode('hex')

cipherfile = open('ciphertext.txt','w')
cipherfile.write(c)