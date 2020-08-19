from Crypto.Util.number import *
from functools import reduce
import operator
from output import enc

# enc = 5550332817876280162274999855997378479609235817133438293571677699650886802393479724923012712512679874728166741238894341948016359931375508700911359897203801700186950730629587624939700035031277025534500760060328480444149259318830785583493

def comb(n, k):
	if k > n :
		return 0
	k = min(k, n - k)
	u = reduce(operator.mul, range(n, n - k, -1), 1)
	d = reduce(operator.mul, range(1, k + 1), 1)
	return u // d 


def enc_to_m(enc):
    mbits = ''
    two = 0 
    while enc > 0:
        if enc % 3 == 0:
            mbits = f'{two}{mbits}'
        elif enc % 3 == 1:
            mbits = f'{1-two}{mbits}'
            two = 0
        else:
            mbits = f'{1-two}{mbits}'
            two = 1
        enc //= 3
    return int(mbits, 2)


def m_to_msg(m, n, k):
    m = bin(m)[2:]
    msg = 0
    for i in range(2, n+1):
        if m[i-1] == '1':
            msg += comb(n-i, k)
            k -= 1

    return msg


 
m = enc_to_m(enc)
n = len(bin(m)[2:])
for k in range(n):
    msg = m_to_msg(m, n, k)
    try:
        msg = bytes.fromhex(f'{msg:x}')
        if b'CCTF{' in msg:
            print(msg)
            break
    except:
        pass
