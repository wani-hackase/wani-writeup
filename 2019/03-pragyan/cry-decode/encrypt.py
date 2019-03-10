import random

file = open("secret.txt","r")
secret = file.read()

flag = ""
for i in secret:
    if i.isalpha():
        flag += i
l = len(flag)

key = [[int(random.random()*10000) for e in range(2)] for e in range(2)]

i = 0
ciphertext = ""

while i <= (l-2):
    x = ord(flag[i]) - 97
    y = ord(flag[i+1]) - 97
    z = (x*key[0][0] + y*key[0][1])%26 + 97
    w = (x*key[1][0] + y*key[1][1])%26 + 97
    ciphertext = ciphertext + chr(z) + chr(w)
    i = i+2

cipherfile = open('ciphertext.txt','w')
cipherfile.write(ciphertext)