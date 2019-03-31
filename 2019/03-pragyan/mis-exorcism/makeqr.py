from PIL import Image, ImageDraw
from pyzbar.pyzbar import decode

def xor_strings(s, t):
    if isinstance(s, str):
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))
    else:
        return bytes([a ^ b for a, b in zip(s, t)])

with open('01qr', 'r') as f:
    qr = f.read()
    qr = qr.split('\n')
    usepadding = False

    h, w = len(qr)-1,len(qr[0])
    H, W = 500, 500

    image = Image.new('RGB', (H, W), (255,255,255))
    black = Image.new('RGB', (5, 5), (255,255,255))
    white = Image.new('RGB', (5, 5), (255,255,255))

    black_d = ImageDraw.Draw(black)
    white_d = ImageDraw.Draw(white)
    black_d.rectangle((0, 0, 5 ,5), fill=(0,0,0))
    white_d.rectangle((0, 0, 5 ,5), fill=(255,255,255))

    if usepadding:
        padding = (W-len(qr[0])*5)//2
    else:
        padding = 0

    for i in range(h):
        for j in range(w):
            if(qr[i][j] == '0'):
                image.paste(black, (padding+j*5, padding+i*5))
            else:
                image.paste(white, (padding+j*5, padding+i*5))

    ans = ''
    d = decode(image)[0][0].decode()
    for a, b in zip(d[::2], d[1::2]):
        ans += chr(int(a+b, 16))

    ans = ''.join(ans)
    print(d)
    print(ans)
    print(xor_strings(ans, 'flagflagflagflagflagflagflagflag'))
