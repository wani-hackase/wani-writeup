from PIL import Image
import datetime
import random
from ctflib import *

dt = datetime.datetime(2019,8,6,11,44,15).timestamp()

random.seed(int(dt))

img = Image.open("./steg_emiru.png")
w, h = img.size

flag = ''
seg = ''
for x in range(w):
    for y in range(h):
        pixel = img.getpixel((x, y))
        rnd = random.randint(0, 2)
        seg += str(pixel[rnd] & 0x01)
        if len(seg) == 8:
            tmp = int(seg[::-1], 2)
            flag += its(tmp)
            seg = ''

print(set(extract_flag(flag, 'KosenCTF{', '}')).pop())
