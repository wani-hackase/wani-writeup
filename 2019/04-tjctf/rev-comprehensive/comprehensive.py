m = 'tjctf{?????????????????}'.lower()
k = '????????'.lower()

f = [[ord(k[a]) ^ ord(m[a+b]) for a in range(len(k))] for b in range(0, len(m), len(k))]
g = [a for b in f for a in b]
h = [[g[a] for a in range(b, len(g), len(f[0]))] for b in range(len(f[0]))]
i = [[h[b][a] ^ ord(k[a]) for a in range(len(h[0]))] for b in range(len(h))]
print(str([a + ord(k[0]) for b in i for a in b])[1:-1] + ',', sum([ord(a) for a in m]))