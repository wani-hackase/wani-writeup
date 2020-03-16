import gmpy2

e = 0x10001

with open('flag.enc', 'rb') as f:
    flag = f.read()

flag = int.from_bytes(flag, byteorder='little')
m, exact = gmpy2.iroot(flag, e)
m = int(m)

if exact:
    flag = m.to_bytes(m.bit_length()//8+1, byteorder='little')
    print(flag)
else:
    print('Failed')
