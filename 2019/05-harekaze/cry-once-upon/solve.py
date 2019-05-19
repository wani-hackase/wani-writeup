from ctflib import *
import numpy as np
import binascii

def dec(a):
    a = np.ravel(a)
    m = [chr(c%251) for c in a]
    print(''.join(m))

c = binascii.unhexlify(b'ea5929e97ef77806bb43ec303f304673de19f7e68eddc347f3373ee4c0b662bc37764f74cbb8bb9219e7b5dbc59ca4a42018')
one, two = c[:25], c[25:]

invB = np.array([[247,11,-194,121,-148],[-935,41,757,-278,332],[-198,63,126,-36,36],[-59,20,67,-23,-4],[932,-110,-733,248,-221]])
invB *= inv(243, 251)

C_1 = [[one[i*5+j] for j in range(5)] for i in range(5)]
C_2 = [[two[i*5+j] for j in range(5)] for i in range(5)]

dec(np.dot(C_1, invB))
dec(np.dot(invB, C_1))
dec(np.dot(C_2, invB))
dec(np.dot(invB, C_2))
