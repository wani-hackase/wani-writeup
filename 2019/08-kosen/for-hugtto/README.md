# InterKosenCTF writeup
## Hugtto! [Forensics, 238pts, 32 solved]
### 問題
Wow! It's random!


### 解法
乱数のシードがsteg_emiru.pngが出力された時間の少し前であることが分かるので、`stat steg_emiru.png` とかで作成日時を調べます。すると以下の結果が得られました。
`Modify: 2019-08-06 11:44:18.000000000 +0900`
この時間から1秒ずつ遡って復号を試みます。すると2019-08-06 11:44:15が正解でした。

```python
from PIL import Image
import datetime
import random

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
            flag += tmp.to_bytes((tmp.bit_length()+7)//8, byteorder='big').decode()
            seg = ''

print(flag)
```

Flag: `KosenCTF{Her_name_is_EMIRU_AISAKI_who_is_appeared_in_Hugtto!PreCure}`
