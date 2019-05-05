from pwn import *
import sympy

r = remote('zerois-o-reiwa.seccon.jp', 23615)
for i in range(1000):
    print('----{}----'.format(i))
    res = r.recv(10 ** 12).decode('utf-8')
    print('res', res)
    if i % 2 == 1:
        print('i', i)
        calculated = sympy.solve(res.split('\n')[0].replace('0=', '').replace('?', 'x'))
        ans = 0 if len(calculated) == 0 else calculated[0]
        print('cal', res.split('\n')[0].replace('0=', ''))
        print('ans', ans)
        r.sendline(str(ans).encode())
