f = open('encrypted')
enc = f.read().strip()
f.close()
L = len(enc)

for k in range(1, L):
    for a in range(L):
        for b in range(L):
            if a == b:
                continue
            flag = list(enc)
            i = k
            for _ in range(L):
                s = (i+a)%L
                t = (i+b)%L
                flag[s], flag[t] = flag[t], flag[s]
                i = (i+k)%L
            flag = ''.join(flag)
            if flag.startswith('KosenCTF{'):
                print(flag)
                break
