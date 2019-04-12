from pwn import *
from base64 import b64decode
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

io = remote('p1.tjctf.org', '8005')

circles = None
gray = None
img = None
for _ in range(100):
    print('[+] {}'.format(_))
    response = io.recvline().decode()
    print('[+]', response)
    if response[4:].startswith('Wrong'):
        if circles is not None:
            for x, y, radius in circles:
                print('center: ({}, {}), radius: {}'.format(x, y, radius))
                cv2.circle(img, (x, y), radius, (0, 255, 0), 1)
                cv2.circle(img, (x, y), 2, (0, 0, 255), 1)

            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.show()

    io.recvline()
    if _ >= 1:
        io.recvline()
    with open('./img/polkadot{}.jpg'.format(_), 'wb') as f:
        s = io.recvline().decode().replace('\n', '').replace('Find the minimum distance between the centers of two circles to continue:','').encode()
        f.write(b64decode(s))


    img = cv2.imread('./img/polkadot{}.jpg'.format(_))
    gray = cv2.inRange(img, (100,100,100), (255, 255, 255))
    gray = cv2.GaussianBlur(gray, (11, 11), 0)


    for dist in range(2000,10, -1):
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, dist/10.0, param1=50, param2=20, minRadius=5, maxRadius=40)
        circles = np.squeeze(circles, axis=0)
        if len(circles) >= 25:
            ans = str(dist/10.0)
            print(ans)
            io.sendline(ans)
            break

        prev = dist


io.interactive()
