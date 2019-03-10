# Pragyan CTF 2019 "Decode This" writeup

This problem is solved by hi120ki.

## check problem

```
Ram has something to show you, which can be of great help. It definitely contains the piece of text "pctf" and whatever follows it is the flag. Can you figure out what it is?

Note: Enclose it in pctf{}
```

There is "pctf" character in secret.txt.

```python
import random

file = open("secret.txt","r")
secret = file.read()

# convert flag to only alphabets
flag = ""
for i in secret:
    if i.isalpha():
        flag += i
l = len(flag)

# generate random number
key = [[int(random.random()*10000) for e in range(2)] for e in range(2)]

i = 0
ciphertext = ""

while i <= (l-2):
    # x and y is 0..25
    x = ord(flag[i]) - 97
    y = ord(flag[i+1]) - 97
    z = (x*key[0][0] + y*key[0][1])%26 + 97
    w = (x*key[1][0] + y*key[1][1])%26 + 97
    ciphertext = ciphertext + chr(z) + chr(w)
    i = i+2

cipherfile = open('ciphertext.txt','w')
cipherfile.write(ciphertext)
```

Flag is converted to only alphabets.

This crypto is called Affin cipher.

<https://en.wikipedia.org/wiki/Affine_cipher>

But this code has some difference.

## solve problem

First, key can be thought as key%26.

```python
a = key[0][0]%26 # a is 0..25
b = key[0][1]%26 # b is 0..25
c = key[1][0]%26 # c is 0..25
d = key[1][1]%26 # d is 0..25
```

Second, There is "pctf" character in secret.txt.

I try all key, and encrypt "pctf", and make sure ciphertext matches.

If it maches, I decode all ciphertext.

```python
cipher_txt = open("ciphertext.txt").read()
cipher_num = []

for i in range(72):
    cipher_num.append(ord(cipher_txt[i]) - 97)

p_num = ord("p") - 97
c_num = ord("c") - 97
t_num = ord("t") - 97
f_num = ord("f") - 97

# try all key
for a in range(26):
    for b in range(26):
        for c in range(26):
            for d in range(26):
                for i in range(34):
                    # make sure ciphertext matches
                    res1 = (a * p_num + b * c_num) % 26
                    res2 = (c * p_num + d * c_num) % 26
                    res3 = (a * t_num + b * f_num) % 26
                    res4 = (c * t_num + d * f_num) % 26
                    if (
                        (cipher_num[i * 2] == res1)
                        and (cipher_num[i * 2 + 1] == res2)
                        and (cipher_num[i * 2 + 2] == res3)
                        and (cipher_num[i * 2 + 3] == res4)
                    ):
                        print("\nkey is", a, b, c, d)
                        # decode all ciphertext
                        for item in range(36):
                            for x in range(26):
                                for y in range(26):
                                    if (
                                        (cipher_num[item * 2] == (a * x + b * y) % 26)
                                        and (cipher_num[item * 2 + 1] == (c * x + d * y) % 26)
                                    ):
                                        print(chr(x + 97), chr(y + 97), end=" ")

# key is 15 10 18 17
# r a m h a s a l i t t l e s e c r e t f o r y o u r i g h t h e r e i t i s p c t f i l i k e c l i m b i n g h i l l s w h a t a b o u t y o u
```

Ram has a little secret for you right here it is pctf i like climbing hills what about you

I get flag : pctf{ilikeclimbinghillswhataboutyou}
