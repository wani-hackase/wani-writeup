# VolgaCTF 2019 Qualifier "Blind" writeup

## Description

Blind
Pull the flag...if you can.

nc blind.q.2019.volgactf.ru 7070

[server.py](server.py)


## Solution



server.py を見てみると、
* ls
* dir
* cd
* cat
* sign

のコマンドを受け付けていることが分かる。
この中で `cd` と `cat` は、そのコマンドのRSA署名をコマンドの先頭につけなければ実行されないことが分かる。

この署名は `sign` コマンドで行えるが、 `cd` と `cat` に対して署名してもらおうとすると、条件分岐で弾かれてしまう。server.py の中で e, n が与えられているので、ここから d を計算できれば署名できるが、n は十分大きく素因数分解は難しい。また e も適切な大きさであることから、直接 d を求めるのは難しいと考えた。


しばらく考えた後に、相手に署名させることが出来るという事と、問題名から Blinding Attack が使えそうだと思いついた。

Blinding Attack で、署名させたい平文 m 以外の別の平文 m' に署名させ、そこから元の平文に対する署名 m^d を手に入れることが出来る。

具体的には次の手順を踏む。

1. r, nが互いに素(⇔ gcd(r, n) = 1)となるような r を ランダムに選ぶ
2. m' ≡ mr^e (mod n), r^{-1} (mod n) を計算する
3. s' ≡ (m')^d (mod n) を得る
4. s ≡ s'r' ≡ m^d (mod n) を得る。

（s は平文mに対する署名、 s'は平文m'に対する署名）

(1.)
randint などで、nと互いに素になるまでrを選び直す。

(2.)
`'cat flag'`をhexエンコードして10進数に直したものをmとする。
`m = int('cat flag'.encode('hex'), 16)`

また、
`m_ = m * pow(r, e, n) % n`
`r_ = inv(r, n))`
ただし、invは ax≡1 (mod b) となるxを返す。

(3.)
`sign` コマンドで偽の平文 m' を送る前に、これをbase64でエンコードする。

(4.)
返ってきた値をs'として
s'r' (mod n)を計算すると、これが元の平文(`'cat flag'`)に対する署名となっている。
`s = s_ * r_ % n`
この値を署名として付けることでFlagを読むことが出来る。

```python
from random import randint
from gmpy2 import gcd
from pwn import *
from base64 import b64encode

def ext_gcd(a, b):
    c0, c1 = a, b
    a0, a1 = 1, 0
    b0, b1 = 0, 1

    while c1 != 0:
        q, m = divmod(c0, c1)
        c0, c1 = c1, m
        a0, a1 = a1, (a0 - q*a1)
        b0, b1 = b1, (b0 - q*b1)
    return a0, b0, c0

def inv(a, n):
    s, _, _ = ext_gcd(a, n)
    return s%n

def blinding_attack(n, e, m):
    r = None
    while True:
        a = randint(2, n-1)
        if gcd(a, n) == 1:
            r = a
            break

    m_ = pow(r, e, n) * m % n
    r_ = inv(r, n)
    return m_, r_

def int_to_str(x):
    x = hex(x)[2:]
    s = ''
    for a, b in zip(x[::2], x[1::2]):
        s += chr(int(a+b, 16))
    return s

n = 26507591511689883990023896389022361811173033984051016489514421457013639621509962613332324662222154683066173937658495362448733162728817642341239457485221865493926211958117034923747221236176204216845182311004742474549095130306550623190917480615151093941494688906907516349433681015204941620716162038586590895058816430264415335805881575305773073358135217732591500750773744464142282514963376379623449776844046465746330691788777566563856886778143019387464133144867446731438967247646981498812182658347753229511846953659235528803754112114516623201792727787856347729085966824435377279429992530935232902223909659507613583396967
e = 65537

cmd_hex = int('cat flag'.encode('hex'), 16)

sign = blinding_attack(n, e, cmd_hex)
m_, r_ = sign

bogus = b64encode(int_to_str(m_))

io = remote('blind.q.2019.volgactf.ru', '7070')

# Enter your command:
io.recvline()
io.sendline('sign sign')

# Enter your command to sign:
io.recvline()
io.sendline('{}'.format(bogus))

s_ = io.recvline()
io.recvline()
s_ = int(s_)

signed_cmd = s_*r_%n
io.sendline('{} cat flag'.format(signed_cmd))

io.interactive()
```

Flag: `VolgaCTF{Bl1nd_y0ur_tru3_int3nti0n5}`
