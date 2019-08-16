# InterKosenCTF writeup
## Temple of Time [Forensics, 285pts, 25 solved]
### 問題
We released our voting system and it's under attack. Can you investigate if the admin credential is stolen?


### 解法
pcapファイルをWiresharkで開いて、プロトコルをHTTPに絞って調べていくと、Time-based SQL Injectionをしているっぽいのが見えます。adminのパスワードを先頭から一文字ずつ総当りして、文字が一致したらsleepさせているのが分かります。リクエストからレスポンスまで時間がかかっているところを調べてみると、1文字目が'K'、2文字目が'o'だったので行けそうです。後はcsvに出力してスクリプトを書きました。

```python
import pandas as pd
import urllib.parse
import re
df = pd.read_csv('data.csv')
data = df[df['Protocol'] == 'HTTP']
data.reset_index(inplace=True)


time, source, destination, info = data['Time'], data['Source'], data['Destination'], data['Info']
r = re.compile(r"\d+")

flag = ''
for i in range(1, len(data)):
    for j in range(i+1, len(data)):
        if source.iloc[j] == destination.iloc[i] and destination.iloc[j] == source.iloc[i]:
            if time.iloc[j]-time.iloc[i] >= 0.1:
                s = urllib.parse.unquote(info[i])
                if s.startswith('GET /index.php'):
                    flag += chr(int(re.findall(r, s)[2]))
                    print(f'[+] Flag: {flag}')
            i += j-i+1
            break
```


Flag: `KosenCTF{t1m3_b4s3d_4tt4ck_v31ls_1t}`
