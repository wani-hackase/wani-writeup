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
