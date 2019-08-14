from secrets import flag
from Crypto.Util.number import getStrongPrime

p = getStrongPrime(512)
q = getStrongPrime(512)
n = p * q

key = int.from_bytes(flag, "big")
c = pow(1 + n, key, n * n)

print("I encrypted my secret!!!", flush=True)
print(c, flush=True)

# receive plaintext
print(
    "I encrypt your message ;)",
    flush=True,
)

while True:
    plaintext = input("> ")
    m = int(plaintext)
    
    # check plaintext
    if m.bit_length() < key.bit_length():
        print(
            "[!]Your plaintext is too weak. At least {} bits long plaintext is required.".format(
                key.bit_length()
            ),
            flush=True,
        )
        continue
        
    # encrypt
    c = pow(1 + n, m, n * n)

    # output
    print("Thanks. This is your secret message.", flush=True)
    print(c, flush=True)
