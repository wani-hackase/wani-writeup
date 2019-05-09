import binascii
import random

from secret import flag

image = int(binascii.hexlify(flag), 16)

palette = 1 << 2048
base = random.randint(0, palette) | 1
secret = random.randint(0, palette)
my_mix = pow(base, secret, palette) # my_mix, base, palette はわかってて、 my_mix = (base ** secret) mod palette

print('palette: {}'.format(palette))
print('base: {}'.format(base))
print('my mix: {}'.format(my_mix))

your_mix = int(input('your mix: '))

shared_mix = pow(your_mix, secret, palette) # your_mix, palette はわかってて、上記の式を解ければsecretがわかり、shared_mixがわかる
painting = image ^ shared_mix # painting はわかってる
print('painting: {}'.format(painting))