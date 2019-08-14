from secret import flag
from random import randrange


def is_prime(N):
    if N % 2 == 0:
        return False
    i = 3
    while i * i < N:
        if N % i == 0:
            return False
        i += 2
    return True


L = len(flag)
assert is_prime(L)

encrypted = list(flag)
k = randrange(1, L)
while True:
    a = randrange(0, L)
    b = randrange(0, L)

    if a != b:
        break

i = k
for _ in range(L):
    s = (i + a) % L
    t = (i + b) % L
    encrypted[s], encrypted[t] = encrypted[t], encrypted[s]
    i = (i + k) % L

encrypted = "".join(encrypted)
print(encrypted)
