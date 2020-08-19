from itertools import product
with open('output.txt') as f:
    s = f.read().strip()

for i, j in product(range(10), repeat=2):
    try:
        bits = '1'*i + s + '1'*j
        x = bytes.fromhex(f'{int(bits, 2):x}')
        if b'CCTF{' in x:
            print(x)
            break
    except:
        pass
